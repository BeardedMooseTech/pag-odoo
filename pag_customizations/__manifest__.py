# -*- coding: utf-8 -*-
{
    'name': "PAG Customizations",
    'version': '18.0.1.0',
    'summary': "Precision Aviation Group Customizations",
    'description': """
Module containing customizations for Precision Aviation Group
    """,
    'author': "Beareded Moose Technologies",
    'website': "https://www.beardedmoosetech.com",
    'category': 'Project',
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
