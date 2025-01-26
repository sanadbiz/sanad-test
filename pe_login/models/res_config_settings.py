from odoo import models, fields, api,_
import secrets
import string
import pyperclip


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ms_access_key = fields.Char(string='Access Key', placeholder='Add Access Key Here',
                                config_parameter='product.ms_access_key')

    def generate_secure_key(self):
        """Generate a secure random key"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        secure_key = ''.join(secrets.choice(alphabet) for _ in range(32))
        self.write({'ms_access_key': secure_key})
        self.env['ir.config_parameter'].sudo().set_param('product.ms_access_key', secure_key)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'New secure key has been generated',
                'sticky': False,
                'type': 'success',
                'next': {
                    'tag': 'reload',
                    'type': 'ir.actions.client',

                }
            }
        }


    def action_copy_key(self, *args, **kwargs):
        ms_access_key = self.ms_access_key or "No key available"
        pyperclip.copy(ms_access_key)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'ms_access_key': 'ms_access_key',
                'type': 'success',
                'title': _('Copied!'),
                'message': _('Key has been copied to clipboard'),
                'sticky': False,

            }
        }