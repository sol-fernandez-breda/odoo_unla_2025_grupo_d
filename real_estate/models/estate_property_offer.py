from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Aceptada"),
            ("refused", "Rechazada")
        ],
        string="Estado"
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Ofertante",
        required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Propiedad",
        required=True
    )
    validity = fields.Integer(
        string="Validez (días)",
        default=7
    )
    date_deadline = fields.Date(
        string="Fecha límite",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                base_date = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - base_date).days

    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Tipo de propiedad",
        related="property_id.property_type_id",
        store=True
    )

    def action_accept_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Esta oferta ya fue aceptada.")

            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

            offer.property_id.state = "oferta_aceptada"

            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
            other_offers.write({"status": "refused"})

            
            offer.status = "accepted"

