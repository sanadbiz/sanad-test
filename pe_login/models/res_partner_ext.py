from odoo import models, fields


class ResUsersExt(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    account_type = fields.Selection([
        ('influencer', 'Influencer'),
        ('brand', 'Brand'),
    ], string="Account Type")
    brand_name = fields.Char(string='Brand Name')
