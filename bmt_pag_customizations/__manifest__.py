# -*- coding: utf-8 -*-
{
    'name': "BMT Project Customizations",
    'version': '18.0.1.0',
    'summary': """Customizations for Project Task.""",
    'description': """BMT Project Addons""",
    'author': "Bearded Moose Technology - Sonali",
    'website': "www.beardedmoosetech.com",
    'category': 'MRP',
    'depends': ['project'],
    'data': [
            "security/ir.model.access.csv",
            "data/progress_task.xml",
            "views/progress_task.xml",
            "views/project_task_view.xml"
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
