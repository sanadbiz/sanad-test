from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class IrMailServerExt(models.Model):
    _inherit = 'ir.mail_server'

    is_use_for_confirmation = fields.Boolean(string='Is Use for Confirmation ?')

    @api.constrains('is_use_for_confirmation')
    def _check_unique_confirmation_server(self):
        """
        Validate that only one mail server can have is_use_for_confirmation set to True
        """
        for record in self:
            if record.is_use_for_confirmation:
                # Count other records with is_use_for_confirmation set to True
                existing_servers = self.search([
                    ('id', '!=', record.id),  # Exclude current record
                    ('is_use_for_confirmation', '=', True)
                ])

                if existing_servers:
                    raise ValidationError(
                        "Only one mail server can be used for confirmation. "
                        "Another mail server is already set for confirmation."
                    )
