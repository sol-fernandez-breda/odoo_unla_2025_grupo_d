from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Propiedades"

    name = fields.Char(string="Título", required=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Tipo Propiedad",
        required=True
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Comprador",
    )
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendedor",
        index=True,
        tracking=True,
        default=lambda self: self.env.user,
        copy=False,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Etiquetas"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Ofertas"
    )

    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha disponibilidad",default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta", copy=False)
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardín")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "Norte"),
            ("south", "Sur"),
            ("east", "Este"),
            ("west", "Oeste"),
        ],
        string="Orientación del jardín",
        default="north",
    )
    garden_area = fields.Integer(string="Superficie jardín")

    state = fields.Selection(
        selection=[
            ("nuevo", "Nuevo"),
            ("oferta_recibida", "Oferta recibida"),
            ("oferta_aceptada", "Oferta aceptada"),
            ("vendido", "Vendido"),
            ("cancelado", "Cancelado"),
        ],
        string="Estado",
        required=True,
        default="nuevo",
        copy=False
    )
    
