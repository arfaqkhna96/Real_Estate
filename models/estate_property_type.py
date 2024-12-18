from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _sql_constraints = [('unique_tag', 'unique(name)', 'Duplicate tags found')]
    _order = 'name'

    name = fields.Char(string="Name" , required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Number of Offers', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)