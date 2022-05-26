from odoo import models,fields

class hms_department (models.Model):
    _name="hms.department"
    name = fields.Char()
    is_opened = fields.Boolean()
    capacity = fields.Integer()
    patient_ids = fields.One2many(comodel_name="hms.patient",inverse_name="department_id")
