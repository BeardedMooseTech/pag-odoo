# -*- coding: utf-8 -*-
from odoo import fields, models, tools
#PG-16-Tasks-and-Sub-tasks-Expanded-View
class ReportProjectTaskUser(models.Model):
    _inherit = 'report.project.task.user'

    parent_task_id = fields.Many2one('project.task', string='Parent Task')
    child_ids = fields.Many2many('project.task', relation='project_task_related_task_rel', column1='task_id',
        column2='related_task_id', string='Subtask',store=True)
    task_status = fields.Many2one('progress.task',string='Status') 
    #PG-43-Remove-decimal-places-from-Scorecard
    actual_1 = fields.Float(string="Actual",digits=(16, 0))
    plan_1 = fields.Float(string="Plan",digits=(16, 0))


    def _select(self):
        return super()._select() +  """,
                t.task_status,
                t.actual_1,
                t.plan_1,
                t.parent_task_id
        """

    def _group_by(self):
        return super()._group_by() + """,
                t.task_status,
                t.actual_1,
                t.plan_1,
                t.parent_task_id
        """

    