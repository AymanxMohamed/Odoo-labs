from odoo import models,fields

class hms_logs (models.Model):
    _name = "hms.logs"
    patient_id = fields.Many2one('hms.patient','Patient')
    created_by= fields.Many2one('res.users', 'Created by', default=lambda self: self.env.user)
    date = fields.Datetime('DateTime', default=lambda self: fields.datetime.now())
    description = fields.Text()