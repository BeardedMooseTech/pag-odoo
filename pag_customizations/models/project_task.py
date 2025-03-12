# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
from lxml import etree
#PAG-2-Project-Tasks-Changes
class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = "name asc"


    task_status = fields.Many2one('progress.task',string='Status',tracking=True) 
    actual_1 = fields.Float(string="Actual",tracking=True)
    actual_2 = fields.Float(string="Actual 2",tracking=True)
    rollup_type = fields.Selection([('1','Avg'),('2','YTD'),('3','Last Actual (Numeric)'),('4','Last Actual (Percentage)')],string="Rollup Type",tracking=True)
    plan_1 = fields.Char(string="Plan",tracking=True)
    plan_2 = fields.Char(string="Plan 2",tracking=True)
    status_id = fields.Char(related='task_status.name',string="Status Name")
    
    #PG-4-Custom-security-on-Planned-fields-on-Progress-tab
    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        if res['views'].get('form'):
            arch = res['views']['form']['arch']
            user = self.env.user
            if not user.has_group('pag_customizations.group_user_plans'):
                arch = etree.fromstring(arch)  
                for node in arch.iterfind(".//field[@name='child_ids']/list/field[@name='plan_1']"):
                    node.set("readonly", "1")
                #for node in arch.iterfind(".//field[@name='child_ids']/list/field[@name='plan_2']"):
                #    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "1")
                #for node in arch.iterfind(".//field[@name='plan_2']"):
                #   node.set("readonly", "1")
                    
                res['views']['form']['arch'] = etree.tostring(arch, encoding='unicode')
        if res['views'].get('list'):
            arch = res['views']['list']['arch']
            user = self.env.user
            if not user.has_group('pag_customizations.group_user_plans'):
                arch = etree.fromstring(arch)  
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "1")
                #for node in arch.iterfind(".//field[@name='plan_2']"):
                #    node.set("readonly", "1")

                res['views']['list']['arch'] = etree.tostring(arch, encoding='unicode')
        return res

    #PG-10-Sub-tasks-list-changes
    @api.depends('child_ids.actual_1', 'child_ids.write_date', 'rollup_type')
    def _compute_roll_up_values(self):
        for task in self:
            if not task.child_ids:
                continue  # Skip tasks without subtasks

            sub_tasks = task.child_ids.filtered(lambda t: not t.child_ids)  # Only bottom-level children
            if not sub_tasks:
                continue  
            if task.rollup_type == '1':
                task.actual_1 = "{:.2f}".format(sum(sub_tasks.mapped('actual_1')) / len(sub_tasks) if sub_tasks else 0.0)
                #task.actual_2 = sum(sub_tasks.mapped('actual_2')) / len(sub_tasks) if sub_tasks else 0.0

            elif task.rollup_type == '2':
                task.actual_1 = "{:.2f}".format(sum(sub_tasks.mapped('actual_1')))
                #task.actual_2 = sum(sub_tasks.mapped('actual_2'))

            elif task.rollup_type in ('3', '4'):
                latest_task = sub_tasks.sorted(lambda t: t.write_date, reverse=True)[:1]
                if latest_task:
                    task.actual_1 = latest_task.actual_1 or 0.0
                    #task.actual_2 = latest_task.actual_2 or 0.0

            # Set parent task status to the status of the most recently updated sub-task
            last_updated_task = sub_tasks.sorted(lambda t: t.write_date, reverse=True)[:1]
            task.task_status = last_updated_task.task_status if last_updated_task else False

    #PG-10-Sub-tasks-list-changes
    @api.onchange('rollup_type')
    def _onchange_rollup_type(self):
        """Recalculate actual_1 and actual_2 when roll_up_type is changed"""
        self._compute_roll_up_values()

    #PG-10-Sub-tasks-list-changes
    def write(self, vals):
        """ Detect changes in actual_1, and status fields to update parent task """
        fields_to_check = {'actual_1', 'task_status'}
        tasks_to_update = self.filtered(lambda task: any(field in vals for field in fields_to_check))
        result = super(ProjectTask, self).write(vals)
        self.env.cr.commit()

        # Trigger parent update after saving sub-task changes
        for task in tasks_to_update:
            if task.parent_id:
                task.parent_id._compute_roll_up_values()

        return result


    