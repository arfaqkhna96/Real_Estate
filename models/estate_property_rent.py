from odoo import fields, models, api


class EstatePropertyRent(models.Model):
    _name = "estate.property.rent"
    _description = "Properties For Rent Saved Here"

    name = fields.Char(string='Property Name', required=True)
    rent_type = fields.Selection([('monthly', 'Monthly'),
                                  ('quarterly', 'Quarterly'),
                                  ('half_yearly', 'Half Yearly'),
                                  ('yearly', 'Yearly'),
                                  ], string='Rent Type', default='monthly', required=True)
    security_deposit = fields.Float(string='Security Deposit', required=True, default=0.0)
    electric_meter = fields.Boolean(string='Electric Meter')
    water_meter = fields.Boolean(string='Water Meter')
    lift = fields.Boolean(string='Lift')
    generator = fields.Boolean(string='Generator')
    swimming_pool = fields.Boolean(string='Swimming Pool')
    prop_rent_price = fields.Float(string='Rent Amount', required=True)
    prop_status = fields.Selection([('ready_to_move', 'Ready to Move')], string='Property Status')
    addr_line_1 = fields.Char(required=True)
    addr_line_2 = fields.Char()
    addr_city=fields.Selection([('hyderabad', 'Hyderabad'), ('khammam', 'Khammam')])
    addr_state = fields.Selection([('telangana', 'Telangana'), ('andhra', 'AndhraPradesh')])
    is_occupied = fields.Boolean(string="Occupied Status", default=False)
    addr_zip = fields.Char()
    addr_country=fields.Selection([('india', 'India'), ('nepal', 'Nepal')])
    prop_area = fields.Integer()
    rent_payment_frequency=fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')])
    color = fields.Integer(compute='_compute_color', store=True)

    def _compute_color(self):
        for record in self:
            record.color = 1 if record.is_occupied else 0
    def action_create_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pay',
            'res_model': 'estate.payment',
            'view_mode': 'form',
            'view_id': self.env.ref('Real_Estate.view_estate_rent_payment_form').id,
            'context': {
                'default_property_id': self.id,
            },
            'target': 'new'
        }
