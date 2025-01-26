from lib2to3.fixes.fix_input import context
from pickle import FALSE

from odoo import http
from odoo.http import request
import json
import math

from odoo.osv.expression import TRUE_LEAF


# from odoo.odoo.addons.base.models.ir_qweb import render


class InfluencerController(http.Controller):
    @http.route(['/api/influencers',
                 '/api/influencers/<int:page_number>'],
                type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def handle_influencers(self, **kwargs):
        if request.httprequest.method == 'POST' and request.httprequest.json:
            domain = self._build_domain_to_search_influencer(request.httprequest.json)
        else:
            domain = []

        return self._get_influencers(domain=domain, **kwargs)

    def _get_influencers(self, domain=None, **kwargs):
        try:
            countries_list = []
            domain = domain or []
            page_number = kwargs.get("page_number") or 0
            offset = (page_number - 1) * 10 if page_number is not 0 else 0
            influencers = request.env['influencer.details'].sudo().search(domain, limit=10, offset=offset)
            influencer_list = []
            influencers_count = request.env['influencer.details'].sudo().search_count([])
            countries = request.env['res.country'].with_context(lang='ar_001').sudo().search(
                [('is_show_on_dashboard', '=', True)])
            if countries:
                countries_list = []
                for country in countries:
                    country_data = {
                        'id': country.id,
                        'name': country.name,
                        'code': country.code,
                    }
                    countries_list.append(country_data)
            for influencer in influencers:
                influencer_data = {
                    'id': influencer.id,
                    'name': influencer.name,
                    'email': influencer.email,
                    'phone': influencer.contact_number,
                    'is_tiktok': influencer.is_tiktok,
                    'is_facebook': influencer.is_facebook,
                    'image': f'/web/image/influencer.details/{influencer.id}/image_1920',
                    'is_twitter': influencer.is_twitter,
                    'is_instagram': influencer.is_instagram,
                    'create_date': str(influencer.create_date),
                }
                influencer_list.append(influencer_data)

            return http.Response(
                json.dumps({
                    'status': 'success',
                    'data': influencer_list,
                    'countries': countries_list,
                    'page_count': math.ceil(influencers_count / 10)
                }),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return http.Response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    # @http.route('/api/influencers/search', type='http', methods=['GET', 'POST'], auth='public', csrf=False)
    # def search_influencers(self, **kwargs):
    #     try:
    #         domain = self._build_domain_to_search_influencer(kwargs)
    #         influencers = request.env['influencer.details'].sudo().search(domain)
    #         # context = {
    #         #     'influencers': influencers
    #         # }
    #         # req = request.render('pe_influencer_discovery.search_controller_template', context)
    #         # return req
    #         influencer_list = []
    #         for influencer in influencers:
    #             influencer_data = {
    #                 'id': influencer.id,
    #                 'name': influencer.name,
    #                 'email': influencer.email,
    #                 'phone': influencer.contact_number,
    #                 'is_tiktok': influencer.is_tiktok,
    #                 'is_facebook': influencer.is_facebook,
    #                 'image': f'/web/image/influencer.details/{influencer.id}/image_1920',
    #                 'is_twitter': influencer.is_twitter,
    #                 'is_instagram': influencer.is_instagram,
    #                 'create_date': str(influencer.create_date),
    #             }
    #             influencer_list.append(influencer_data)
    #         return http.Response(
    #             json.dumps({
    #                 'status': 'success',
    #                 'data': influencer_list,
    #             }),
    #             content_type='application/json',
    #             status=200
    #         )
    #
    #     except Exception as e:
    #         return http.Response(
    #             json.dumps({
    #                 'status': 'error',
    #                 'message': str(e)
    #             }),
    #             content_type='application/json',
    #             status=500
    #         )

    def _build_domain_to_search_influencer(self, filters):
        domain = []
        platform_domain = []
        if platform := filters.get('platform'):
            if platform == 'instagram':
                platform_domain = ('is_instagram', '=', True)
            if platform == 'tiktok':
                    platform_domain = ('is_tiktok', '=', True)
            if platform == 'facebook':
                    platform_domain = ('is_facebook', '=', True)
            domain.append(platform_domain)
        # if filters.get('nano') == 'on':  # If 'nano' is selected
        #     domain.append(('minimum_follower', '>', 1000))  # Greater than 1000 followers
        #     domain.append(('minimum_follower', '<', 10000))  # Less than 10000 followers
        # elif filters.get('micro') == 'on':  # If 'micro' is selected
        #     domain.append(('minimum_follower', '>=', 10000))  # Minimum followers for 'micro'
        #     domain.append(('minimum_follower', '<=', 50000))  # Maximum followers for 'micro'
        # elif filters.get('mini') == 'on':  # If 'mini' is selected
        #     domain.append(('minimum_follower', '<=', 50000))  # Maximum followers for 'mini'
        # elif filters.get('mid') == 'on':  # If 'mid' is selected
        #     domain.append(('minimum_follower', '>=', 500000))  # Minimum followers for 'mid'
        # elif filters.get('macro') == 'on':  # If 'mega' is selected
        #     domain.append(('minimum_follower', '>=', 1000000))
        # elif filters.get('mega') == 'on':
        #     domain.append(('minimum_follower', '>=', 1000000))
        # if min_followers := filters.get('followers_min'):
        #     min_followers_domain = [('minimum_follower', '>=', min_followers)]
        #     domain.append(min_followers_domain)
        if gender := filters.get('gender'):
            if gender != 'both':
                domain.append(('gender', '=', gender))
        # if age := filters.get('age'):
        #     age_domain = ('age', '=', age)
        #     domain.append(age_domain)
        if country := filters.get('country'):
            country_id = request.env['res.country'].with_context(lang='ar_001').sudo().search(
                [('name', '=', country)], limit=1)
            country_domain = ('country_id', '=', country_id.id)
            domain.append(country_domain)
        return domain

    @http.route('/web/dashboard', type='http', csrf=False, auth='public', website=True)
    def sanad_dashboard(self):
        """ rendering the temporary form to test the influencer search controller """
        context = {
        }
        req = request.render('pe_influencer_discovery.web_dashboard')
        return req

    @http.route('/web/search', csrf=False, type='http', auth='public', website=True)
    def web_sanad_search(self, *args, **kw):
        # countries = request.env['res.country'].with_context(lang='ar_001').sudo().search([('is_show_on_dashboard', '=', True)])
        return request.render('pe_influencer_discovery.search_result')

    @http.route('/web/dashboard/logout', type='http', auth="user", website=True)
    def logout(self):
        try:
            request.session.logout(keep_db=True)
            return http.local_redirect('/web/login?logout=success')
        except Exception:
            return http.local_redirect('/web/login?logout=failed')
