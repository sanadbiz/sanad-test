import logging
from pickle import FALSE

import werkzeug
from werkzeug.urls import url_encode

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.exceptions import UserError
from odoo.http import request
import hashlib
import logging
import random
from datetime import datetime, timedelta
import json
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)

LOGIN_SUCCESSFUL_PARAMS.add('account_created')


class AuthReset(AuthSignupHome):

    @http.route('/web/reset_password', type='http', auth='public', csrf=False, website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return self.web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    user = request.env['res.users'].sudo().search(
                        [('login', '=', login)], limit=1)
                    if user:
                        token, expiry_time = self._generate_verification_code_forget_password(
                            email=qcontext.get('login'))
                        request.session.update({
                            "email": qcontext.get('login'),
                            'is_from_forget_password': True,
                        })
                        response = request.redirect('/web/retrieve_password')
                        return response
                        # Add any additional logic to send the reset password email here
                    else:
                        qcontext['error'] = _("لم يتم العثور على مستخدم في النظام بهذا التسجيل")
                        return request.render('pe_login.forget_password', qcontext)
            except Exception as e:
                qcontext['error'] = _("An error occurred, please try again later")
                return request.render('pe_login.forget_password')
        else:
            return request.render('pe_login.forget_password')

    def _generate_verification_code_forget_password(self, email):
        token = random.randint(100000, 999999)
        expiry_time = datetime.now() + timedelta(minutes=10)
        check_existing = request.env['auth.temp.store'].sudo().search([('email', '=', email)])
        password = None
        if check_existing:
            password = check_existing.password
            check_existing.unlink()
        request.env['auth.temp.store'].sudo().create({
            'email': email,
            'password': password,
            'token': token,
            'expiry_time': expiry_time,
            'token_hash': hashlib.sha256(str(token).encode()).hexdigest(),
        })
        return token, expiry_time

    @http.route('/web/send_again', type='http', auth='public', website=True, sitemap=False)
    def web_send_confirmation_code_again(self):
        login = request.session.get('email')
        token, expiry_time = self._generate_verification_code_forget_password(
            email=login)
        return request.redirect('/web/retrieve_password')
