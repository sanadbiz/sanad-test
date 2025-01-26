from operator import index

from odoo import fields, api, models
from odoo import SUPERUSER_ID


class AuthTemporaryStore(models.Model):
    _name = 'auth.temp.store'
    _description = 'This Will store for email for temporary to make it more persistent'

    email = fields.Char(index=True)
    token = fields.Char()
    token_hash = fields.Char()
    verified = fields.Boolean()
    expiry_time = fields.Datetime()
    password = fields.Char()

    @api.model
    def _clean_expired_data(self):
        records = self.env['auth.temp.store'].sudo().search([
            ('verified', '=', True)
        ])
        records.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AuthTemporaryStore, self).create(vals_list)
        template = self.env.ref("pe_login.mail_template_email_verification")
        out_going_mail_server = self.env['ir.mail_server'].search([('is_use_for_confirmation', '=', True)])
        if out_going_mail_server:
            email_from = out_going_mail_server.from_filter
            email_values = {
                'email_to': vals_list[0].get('email'),
                'email_from': email_from
            }
            template.sudo().send_mail(res.id, force_send=True, email_values=email_values)
        return res
