# -*- coding: utf-8 -*-
from odoo import fields, models, tools
#PG-16-Tasks-and-Sub-tasks-Expanded-View
class ReportProjectTaskUser(models.Model):
    _inherit = 'report.project.task.user'

    parent_id = fields.Many2one('project.task', string='Parent Task')
    child_ids = fields.Many2many('project.task', relation='project_task_related_task_rel', column1='task_id',
        column2='related_task_id', string='Subtask',store=True)
    