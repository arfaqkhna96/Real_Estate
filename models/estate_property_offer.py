from datetime import  timedelta,datetime
from odoo import fields, models, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name ='estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    state = fields.Selection([('accepted','Accepted'),('refused','Refused')] , copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property' ,required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        string='Property Type',
        store=True
    )
    validity = fields.Integer(string='Validity',default=7)
    date_deadline = fields.Date(store=True, compute='_compute_date_deadline',default=lambda self: (datetime.today() + timedelta(days=7)).date())

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            print(rec.create_date)
            if rec.create_date:  # Check if create_date is a valid datetime
                rec.date_deadline = (rec.create_date + timedelta(days=rec.validity)).date()
            else:
                rec.date_deadline = False

    def action_accept(self):
        for offer in self:
            if offer.property_id.status == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            if any(o.state == 'accepted' for o in offer.property_id.offer_ids):
                raise UserError("Only one offer can be accepted for a property.")
            offer.state = 'accepted'
            offer.property_id.status='offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])

            existing_offers = self.search([('property_id', '=', property.id)])
            if any(offer.price >= vals['price'] for offer in existing_offers):
                raise UserError("The offer must be higher than existing offers.")

            if property.status == 'new':
                property.status = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals_list)