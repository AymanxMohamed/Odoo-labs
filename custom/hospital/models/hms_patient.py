from math import floor
from odoo import api, models,fields
from odoo.exceptions import UserError

class hms_patient (models.Model):
    _name="hms.patient"
    _rec_name="full_name"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True) 
    full_name = fields.Char(string='Full name', compute='_compute_full_name')
    email = fields.Char(required=True)
    birth_date = fields.Date(string='Birth date', default=fields.Date.today())
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([("A+","A+"), ("A-","A-"), ("B+","B+"), ("B-","B-"), ("O+","O+"), ("O-","O-")], default="A+")
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer(compute="calc_age")
    state = fields.Selection([('u', 'Undetermined'),('g', 'Good'),('f', 'Fair'),('s', 'Serious'),], default='u')
    department_id = fields.Many2one("hms.department")
    department_open = fields.Boolean(related="department_id.is_opened")
    doctors_ids = fields.Many2many(comodel_name='hms.doctors')
    logs_ids= fields.One2many(comodel_name='hms.logs', inverse_name='patient_id')
    def next_state(self):
        if self.state == 'u':
            self.state = 'g'
            self.changeState('Good')
        elif self.state == 'g':
            self.state = 'f'
            self.changeState('Fair')

        elif self.state == 'f':
            self.state = 's'
            self.changeState('Serious')

        elif self.state == 's':
            self.state = 'u'
            self.changeState('Undetermined')


    def changeState(self,state):
        self.env['hms.logs'].create({
            'description': "change patient state to " + state,
            'patient_id': self.id
        })
        
    @api.onchange('department_id')
    def onchange_department_id(self):
        if not self.department_open and self.first_name:
            raise UserError("Department not opened")
        
    @api.depends('birth_date')
    def calc_age(self):
        for record in self:
            get_today= fields.Date.today(record)
            get_birthdate= fields.Date.to_date(record.birth_date)
            record.age =floor((get_today - get_birthdate).days/365)
            
    @api.onchange('age')
    def onchange_age(self):
        if self.first_name and self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'take attention', 'message': 'pcr checked for this patient'}} 
        
    _sql_constraints=[
        ('Duplicate_email' , 'UNIQUE(email)','email is already exists')
    ]  
    
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name