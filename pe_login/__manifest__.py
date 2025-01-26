{
    'name': 'pe_login',

    'summary': 'pe_login',

    'version': '17.0.1.0',

    'author': 'Admin',

    'category': 'General',

    'description': 'pe_login',

    'depends': ['base', 'web', 'auth_signup', 'website', 'contacts', 'pe_influencer_discovery', 'http_routing',
                'portal'],

    'sequence': -1,
    'data': [
        'security/ir.model.access.csv',

        # Web
        'views/auth/common_structure.xml',
        'views/auth/login.xml',
        'views/auth/login_portal_ext.xml',
        'views/auth/retrive_password.xml',
        'views/auth/forget_screen.xml',
        'views/auth/create_password.xml',
        'views/auth/signup.xml',
        'views/auth/retrive_password_signup.xml',
        'views/auth/brand_info_screen.xml',
        'views/auth/profile_setting.xml',

        # Model Views
        'views/model_views/res_partner_ext.xml',
        'views/model_views/res_user_ext.xml',
        'views/model_views/res_country_ext.xml',
        'views/model_views/ir_mail_server_ext.xml',

        # Email Templates
        'email_templates/token_email_template.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'pe_login/static/src/css/style.css',
            'pe_login/static/src/js/hide_show.js',
            'pe_login/static/src/js/profile_selection.js',
            'pe_login/static/src/js/controller.js',
            'pe_login/static/src/js/retrive_password.js',
            'pe_login/static/src/js/signup_validation.js',
            'pe_login/static/src/js/forget_screen.js',
        ]

    },

    'installable': True,
    'application': True,
    'auto_install': False,

}
