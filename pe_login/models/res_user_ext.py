from odoo import models, fields, _, api


class ResUsersExt(models.Model):
    _inherit = 'res.users'

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    account_type = fields.Selection([
        ('influencer', 'Influencer'),
        ('brand', 'Brand'),
    ], string="Account Type")
    brand_name = fields.Char(string='Brand Name')
    country_name = fields.Char(string='Country')