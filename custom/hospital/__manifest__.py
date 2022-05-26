{
    'name': 'Hospital',
    'description': """
        Hospital Module
    """,
    'depends':['crm'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/crm_customers_view.xml',
        'reports/user_report.xml',
        'reports/user_template.xml',
    ],
    'license': 'LGPL-3',
}