{
    'name': 'pe_influencer_discovery',

    'summary': 'pe_influencer_discovery',

    'version': '17.0.1.0',

    'author': 'Admin',

    'category': 'General',

    'description': 'pe_influencer_discovery',

    'depends': ['base', 'web', 'auth_signup', 'website', 'http_routing'],

    'sequence': -1,
    'data': [
        'security/ir.model.access.csv',

        # Dashboard
        'views/dashboard/dashboard.xml',
        'views/dashboard/search_result.xml',
        'views/dashboard/influencer_details.xml',
        'views/dashboard/influencer_marketing_campaign.xml',
        # 'views/dashboard/campaign_creation.xml',
        # 'views/dashboard/campaign_landing_page.xml',

    ],

    'assets': {
        'web.assets_frontend': [
            # 'pe_influencer_discovery/static/src/js/controller.js',
            'pe_influencer_discovery/static/src/css/dashboard.css',
            # 'pe_influencer_discovery/static/src/css/campaign_landing.css',

            # Dashboard Javascript Files
            'pe_influencer_discovery/static/src/js/dashboard/js/dashboard.js',
            'pe_influencer_discovery/static/src/js/dashboard/js/search.js',
            'pe_influencer_discovery/static/src/js/dashboard/js/search_controller.js',
            'pe_influencer_discovery/static/src/js/dashboard/js/customized_selection.js',
            'pe_influencer_discovery/static/src/js/dashboard/templates/search_controller_template.xml',
        ]

    },

    'installable': True,
    'application': True,
    'auto_install': False,

}
