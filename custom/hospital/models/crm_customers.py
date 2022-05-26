from odoo import api, models, fields
from odoo.exceptions import UserError


class CrmCustomersInherit(models.Model):
    _inherit = 'res.partner'

    salary = fields.Float()

    vat = fields.Char(required=True)

    related_patient_id = fields.Many2one("hms.patient")


    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("Can't delete customer,this customer have patient")
        super().unlink()

    @api.constrains("email")
    def check_email(self):
        for record in self:
            if record.email == record.related_patient_id.email:
                raise UserError('This email used by patient')
        customers = self.search([('email', '=', self.email)])
        if len(customers) > 1:
            raise UserError('Email already existed')
        return True
