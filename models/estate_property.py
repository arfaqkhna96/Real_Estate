from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
import re
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]
    _order = 'id desc'


    name = fields.Char(string="Name", required=True, default="Unknown")
    category = fields.Selection([('sale','Sale'),('rent','Rent')], required=True, string="Category", default='sale')
    email = fields.Char(string="Email")
    warning_message = fields.Boolean(string="Warning Message", default=False, store=True)
    description = fields.Text(string="Description")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date of Availability", default=lambda self: (datetime.today() + timedelta(days=90)).date())
    expected_price = fields.Float(string="Expected Price", required=True, default=0.00)
    selling_price = fields.Float(string="Selling Price", default=0.00)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)", default=0)
    facades = fields.Integer(string="Facades", default=0)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area(sqm)" , default=0)
    garden_orientation = fields.Selection([('north','North'),('east','East'),('west','West'),('south','South')],string="Garden Orientation")
    status = fields.Selection([('new', 'New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','Cancelled')], default='new', )
    active = fields.Boolean(string="Active", default=False)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson",
                                     default=lambda self: self.env.user, required=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Offers")
    total_area = fields.Float(string="Total Area", compute='_calculate_total_area', store=True)
    availability = fields.Selection(
        [('available', 'Available'), ('sold', 'Sold')],
        string='Availability',
        default='available'
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        for property in self:
            if property.status not in ['new', 'cancelled']:
                raise UserError("You can only delete properties in 'New' or 'Cancelled' state.")


    @api.depends('living_area','garden_area')
    def _calculate_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0) + (rec.garden_area or 0)


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def action_set_sold(self):
        for property in self:
            if property.status == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold.")
            property.status = 'sold'
            property.availability = 'sold'

    def action_set_cancel(self):
        for property in self:
            if property.status == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            property.status = 'cancelled'

    @api.onchange('email')
    def _onchange_email(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if self.email and not re.match(email_pattern, self.email):
            self.warning_message = True
        else:
            self.warning_message = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            minimum_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, minimum_price, precision_rounding=0.01) < 0:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')