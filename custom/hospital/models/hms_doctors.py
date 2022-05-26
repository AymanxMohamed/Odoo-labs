from odoo import api, models,fields

class hms_doctors (models.Model):
    _name="hms.doctors"
    _rec_name = "full_name"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    full_name = fields.Char(string='Full name', compute='_compute_full_name')
    image = fields.Image()
    patients_ids = fields.Many2many(comodel_name='hms.patient',read_only=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name