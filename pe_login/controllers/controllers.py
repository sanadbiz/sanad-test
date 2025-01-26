from http.client import responses

from odoo.addons.web.controllers.home import Home as WebHome
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
import odoo
import odoo.modules.registry
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import werkzeug
from werkzeug.urls import url_encode
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
import hashlib
import logging
import random
from datetime import datetime, timedelta
import json

_logger = logging.getLogger(__name__)

SIGN_UP_REQUEST_PARAMS.update({
    'name_first', 'name_last', 'phone_country', 'phone'
})


class FrontEndController(WebHome):

    @http.route('/web/login', type='http', auth='public', csrf=False, website=True)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        qcontext = self.get_auth_signup_qcontext()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # simulate hybrid auth=user/auth=public, despite using auth=none to be able
        # to redirect users when no db is selected - cfr ensure_db()
        if request.env.uid is None:
            if request.session.uid is None:
                # no user -> auth=public with specific website public user
                request.env["ir.http"]._auth_method_public()
            else:
                # auth=user
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            qcontext['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            qcontext['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                request.session['is_login_success'] = True
                if request.env['res.users'].browse(uid).has_group('base.group_portal'):
                    return request.redirect(self._login_redirect(uid, redirect=redirect))
                else:
                    return request.redirect(self._login_redirect(uid, redirect=redirect))
                # return request.redirect('/web/dashboard')
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    qcontext['error'] = _("البريد الألكتروني او كلمه السر غير صحيحه")
                else:
                    qcontext['error'] = e.args[0]
        # else:
        #     if 'error' in request.params and request.params.get('error') == 'access':
        #         qcontext['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            qcontext['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        if kw and 'debug' in kw:
            response = request.render('web.login', qcontext)
        else:
            response = request.render('pe_login.login', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    @http.route('/v1/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup_v1(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if qcontext.get('password') == qcontext.get('confirm_password'):
            if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                qcontext['error'] = _("المستخدم مسجل بالفعل")
                response = request.render('pe_login.signup', qcontext)
                return response

            token_generated = self._check_token_generated(kw={'email': qcontext.get("login")})

            if token_generated:
                response = request.redirect('/web/retrieve_password')
                return response

            token, expiry_time = self._generate_verification_code(email=kw.get('login'), password=kw.get('password'))

            request.session.update({
                "email": kw.get('login'),
            })
            request.session['is_coming_from_signup'] = True
            response = request.redirect('/web/retrieve_password')
            return response
        qcontext['error'] = _("كلمة المرور وتأكيد كلمة المرور غير متطابقين")
        return request.render('pe_login.signup', qcontext)

    def _generate_verification_code(self, email, password):
        token = random.randint(100000, 999999)
        expiry_time = datetime.now() + timedelta(minutes=10)
        check_existing = request.env['auth.temp.store'].sudo().search([('email', '=', email)])
        if check_existing:
            check_existing.unlink()
        request.env['auth.temp.store'].sudo().create({
            'email': email,
            'token': token,
            'expiry_time': expiry_time,
            'token_hash': hashlib.sha256(str(token).encode()).hexdigest(),
            'password': password
        })
        return token, expiry_time

    def _check_token_generated(self, kw):
        result = request.env['auth.temp.store'].sudo().search([
            ('verified', '=', False),
            ('email', '=', kw.get('login')),
            ('expiry_time', '>', datetime.now())
        ])

        return result

    def _create_client_in_real(self, email, password):
        portal_group = request.env.ref('base.group_portal')
        user = request.env['res.users'].sudo().create(
            {
                'name': email,
                'login': email,
                'password': password,
                'groups_id': [(4, portal_group.id)]  # Add the portal group
            }
        )
        return user

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        # if not qcontext.get('token') and not qcontext.get('signup_enabled'):
        #     raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)

                # Set user to public if they were not signed in by do_signup
                # (mfa enabled)
                if request.session.uid is None:
                    public_user = request.env.ref('base.public_user')
                    request.update_env(user=public_user)

                # Send an account creation confirmation email
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                )
                template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                           raise_if_not_found=False)
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.warning("%s", e)
                    qcontext['error'] = _("Could not create a new account.") + "\n" + str(e)

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search(
                [('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('pe_login.signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    def _prepare_signup_values(self, qcontext):
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password')}
        values['name'] = "sameer"
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang','')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values

    @http.route('/web/retrieve_password', type='http', auth='public', website=True)
    def web_sanad_retrieve_password(self):
        if not request.session.get('is_coming_from_signup') and not request.session.get('is_from_forget_password'):
            return request.render('http_routing.404')
        context = {
            'email': request.session.get('email')
        }
        req = request.render('pe_login.retrieve_password', context)
        return req

    @http.route('/web/create_password', type='http', csrf=False, auth='public', website=True)
    def web_sanad_create_password(self, **kwargs):
        data = request.get_json_data()
        code = data.get('code_structure')

        def search_for_email_verify_code(email, code):
            email_client = self._check_token_generated(kw={'login': email})
            if email_client:
                if email_client.token_hash == hashlib.sha256(''.join(map(str, code)).encode()).hexdigest():
                    if request.session.get('is_from_forget_password') == True:
                        request.session['is_from_forget_password'] = False
                        return json.dumps({
                            "reroute_location": '/web/retrieve_password_signup'
                        })
                    user = self._create_client_in_real(email_client.email, email_client.password)
                    request.session.update({'user_id': user.id})
                    request.session.update({'is_signup_retrieve': True})
                    return json.dumps({
                        "reroute_location": '/web/profile_settings'
                    })
                else:
                    return json.dumps({
                        "error": "invalid_code"
                    })
            else:
                return json.dumps({
                    "error": "invalid_code"
                })

        if code:
            email = data.get('email') or request.session.get('email')
            return search_for_email_verify_code(email, code)
        else:
            return json.dumps({
                "error": "Verification code is missing."
            })

    @http.route('/web/retrieve_password_signup', type='http', csrf=False, auth='public', website=True)
    def web_sanad_retrieve_password_signup(self, **kwargs):
        if request.httprequest.method == 'POST':
            login = request.session.get('email')
            if login:
                request.env['res.users'].sudo().search([('login', '=', login)], limit=1).write(
                    {'password': kwargs['password']})
                return request.redirect('/web/login')
        return request.render('pe_login.create_password')

    @http.route('/web/profile_settings', type='http', csrf=False, auth='public', website=True)
    def web_sanad_profile_settings(self):
        if request.session.get('is_signup_retrieve'):
            request.session.update({'is_signup_retrieve': False})
            return request.render('pe_login.profile_settings')
        return request.render('http_routing.404')

    @http.route('/web/profile_settings_data_filled', csrf=False, type='http', auth='public')
    def profile_settings_data_filled(self):
        data = request.get_json_data()
        profile_setting_value = data.get('profile_setting_value')
        user_id = request.session.get('user_id')
        if user_id:
            user_record = request.env['res.users'].sudo().browse(user_id)
            user_record.write({
                'account_type': profile_setting_value
            })
            request.session['is_profile_setting'] = True
            return json.dumps({
                "reroute_location": '/web/brand_info'
            })

    @http.route('/web/brand_info', csrf=False, type='http', auth='public', website=True)
    def web_sanad_brand_info(self, *args, **kw):
        if request.session.get('is_profile_setting'):
            if request.httprequest.method == 'POST':
                request.session.update({'is_profile_setting': False})
                data = request.get_json_data()
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                brand_name = data.get('brand_name')
                mobile_number = data.get('mobile_number')
                country = data.get('country')

                user_id = request.session.get('user_id')

                if user_id:
                    user_record = request.env['res.users'].sudo().browse(user_id)
                    country_record = request.env['res.country'].sudo().search([('code', '=', country)], limit=1)
                    user_record.write({
                        'first_name': first_name,
                        'last_name': last_name,
                        'name': f"{first_name} {last_name}",
                        'mobile': mobile_number,
                        'brand_name': brand_name,
                        'country_name': country_record.name if country_record else '',
                    })
                    return json.dumps({
                        "reroute_location": '/web/login',
                    })
            countries = request.env['res.country'].sudo().search([('is_show_in_signup', '=', True)])
            return request.render('pe_login.brand_info', {
                'countries': countries
            })
        return request.render('http_routing.404')
