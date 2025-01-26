
from odoo import models, fields


class ResCountryExt(models.Model):
    _inherit = 'res.country'

    is_show_in_signup = fields.Boolean(string='Show on signup page ?')
    is_show_on_dashboard = fields.Boolean(string='Show on dashboard ?')