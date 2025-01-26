from odoo import models, fields


class InfluencerDetails(models.Model):
    _name = 'influencer.details'
    _description = 'Influencer Details'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    email = fields.Char(string='Email')
    verified = fields.Boolean(string='Is Verified ?', default=False)
    country_id = fields.Many2one('res.country', string='Country')
    followers = fields.Float(string='Followers')
    image_1920 = fields.Image(string="Profile Picture", max_width=1920, max_height=1920)
    bio = fields.Char(string='Bio')
    niche = fields.Char(string='Niche')
    average_like = fields.Integer(string='Average Like')
    minimum_rate = fields.Monetary(string='Minimum Rate Per Post', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    minimum_follower = fields.Integer(string='Minimum Followers')
    contact_number = fields.Char(string='Phone')
    city = fields.Char(string='City')
    is_available = fields.Boolean(string='Is Available ?', default=False)
    follower_location = fields.Many2one('res.country',string="Follower Location")
    is_facebook = fields.Boolean(string='Is Facebook ?')
    is_tiktok = fields.Boolean(string='Is Tiktok ?')
    is_twitter = fields.Boolean(string='Is Twitter ?')
    is_instagram = fields.Boolean(string='Is Instagram ?')
    social_media_platform = fields.Selection([
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok')
    ], string="Social Media Platform")

