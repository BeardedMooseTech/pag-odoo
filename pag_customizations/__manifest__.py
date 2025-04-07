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
    'depends': ['project','web','web_hierarchy'],
    'data': [
            "security/ir.model.access.csv",
            "data/progress_task.xml",
            "data/plan_group.xml",
            "views/progress_task.xml",
            "views/project_task_view.xml",
            "views/project_type_view.xml",
            "views/project_project_view.xml",
            "report/scoreboard.xml",
            "wizard/scoreboard_wizard.xml"
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'assets': {
        "web.assets_backend": [
            "pag_customizations/static/src/xml/list.xml",
            "pag_customizations/static/src/js/list_renderer.js",
            "pag_customizations/static/src/js/project_controller.js",
            "pag_customizations/static/src/js/percentage_widget.js",
        ],
    },
    'license': 'LGPL-3',
}
