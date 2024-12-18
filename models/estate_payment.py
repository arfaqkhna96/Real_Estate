from odoo import models, fields, api
from datetime import date


class EstatePayment(models.Model):
    _name = 'estate.payment'
    _description = 'Real Estate Payment'

    reference = fields.Char(string="Reference Number", copy=False)
    property_id = fields.Many2one('estate.property.rent', string="Property", required=True)
    customer_name = fields.Char(string="Customer Name")
    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True)
    payment_mode = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
    ], string="Payment Mode", required=True, default="cash")
    amount = fields.Char(string="Amount")
    pay_for = fields.Selection([('security_deposit','Security Deposit'),('rent','Rent')],string="Payment For")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('estate.payment')
        return super().create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.property_id.name}"

    def action_pay(self):
        pass