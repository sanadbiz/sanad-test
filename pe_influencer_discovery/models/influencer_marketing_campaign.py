from odoo import models, fields


class InfluencerCampaign(models.Model):
    _name = 'influencer.campaign'
    _description = 'Influencer Marketing Campaign'

    name = fields.Char(string='Campaign Name', required=True)
    campaign_tags = fields.Text(string='Campaign Tags')
    is_campaign_private = fields.Boolean(string='Make Campaign Private ?')
    is_add_brief = fields.Boolean(string='Is Add Brief ?')
    pdf_brief_id = (fields.Many2many(
        'ir.attachment',
        string="Pdf Brief"
    ))
    active = fields.Boolean(string='Active', default=True)
    posted = fields.Integer(string='Posted')
    is_enable_store = fields.Boolean(string='Is Enable Store ?')
    is_proposal_acceptance_mandatory = fields.Boolean(string='Is Proposal Acceptance Mandatory ?')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    currency_id = fields.Many2one('res.currency', string='Currency')
    influencer_ids = fields.Many2many('influencer.details', string='Influencers',
                                      domain=[])
    is_instagram = fields.Boolean(string='Instagram')
    is_youtube = fields.Boolean(string='Youtube')
    is_tiktok = fields.Boolean(string='Tiktok')
    content_type = fields.Selection(
        [('post', 'Post'), ('story', 'Story'), ('reel', 'Reel'), ('video', 'Video')],
        string="Content Type"
    )
    budget_per_influencer = fields.Monetary('Budget Per Influencer', currency_field='currency_id')

    campaign_budget = fields.Monetary(string="Budget", currency_field='currency_id')
    budget_spent = fields.Float(string="Budget Spent")
    payment_terms = fields.Text(string="Payment Terms")

    # Content Tracking

    track_your_content = fields.Char(string="Track Your Content")
    discount_code = fields.Char(string="Discount Code")
