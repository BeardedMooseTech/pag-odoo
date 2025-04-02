# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
from lxml import etree
from odoo.exceptions import AccessError

#PAG-2-Project-Tasks-Changes
class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = "name asc"


    task_status = fields.Many2one('progress.task',string='Status',tracking=True) 
    actual_1 = fields.Float(string="Actual",tracking=True)
    actual_2 = fields.Float(string="Actual 2",tracking=True)
    # PG-22-View-as-if-based-metric
    plan_1 = fields.Float(string="Plan",tracking=True)
    #PG-18-Make-Roll-up-Type-not-required-on-parent-level
    rollup_type = fields.Selection([('1','Avg'),('2','YTD'),('3','Last Actual (Numeric)'),('4','Last Actual (Percentage)')],string="Rollup Type",tracking=True)
    plan_2 = fields.Float(string="Plan 2",tracking=True)
    status_id = fields.Char(related='task_status.name',string="Status Name")
    #PG-24-Create-Initiative-field-on-the-project-level
    initiative_id = fields.Many2one('project.type',related='project_id.initiative_id',string='Initiative',store=True)
    project_type = fields.Selection(related='project_id.project_type',string='Project Type',store=True)


    #PG-4-Custom-security-on-Planned-fields-on-Progress-tab
    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        if res['views'].get('form'):
            arch = res['views']['form']['arch']
            arch = etree.fromstring(arch)
            user = self.env.user
            # PG-21-Permissions-change
            if user.has_group('project.group_project_user') and not user.has_group('project.group_project_manager'):
                restricted_fields = ['tag_ids', 'milestone_id', 'project_id']
                for field in restricted_fields:
                    for node in arch.iterfind(f".//field[@name='{field}']"):
                        node.set("options", "{'no_create': True}")

            if not user.has_group('pag_customizations.group_user_plans'):
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
            arch = etree.fromstring(arch)
            user = self.env.user
            # PG-21-Permissions-change
            if user.has_group('project.group_project_user') and not user.has_group('project.group_project_manager'):
                restricted_fields = ['tag_ids', 'milestone_id', 'project_id']
                for field in restricted_fields:
                    for node in arch.iterfind(f".//field[@name='{field}']"):
                        node.set("options", "{'no_create': True}")

            if not user.has_group('pag_customizations.group_user_plans'):
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
        # PG-21-Permissions-change
        if self.env.user.has_group('project.group_project_user') and not self.env.user.has_group('project.group_project_manager'):
            allowed_fields = {'task_status','plan_1','actual_1','rollup_type'}
            if any(field not in allowed_fields for field in vals.keys()):
                raise AccessError("You are only allowed to modify the Progress fields.")

        # Detect changes in actual_1, and status fields to update parent task
        fields_to_check = {'actual_1', 'task_status'}
        tasks_to_update = self.filtered(lambda task: any(field in vals for field in fields_to_check))
        result = super(ProjectTask, self).write(vals)
        if tasks_to_update:
            self.env.cr.commit()
            if self.project_type =='goals':
                # Trigger parent update after saving sub-task changes
                for task in tasks_to_update:
                    if task.parent_id:
                        task.parent_id._compute_roll_up_values()
        return result

     #PG-16-Tasks-and-Sub-tasks-Expanded-View
    def action_open_subtasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subtasks',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('parent_id', '=', self.id)],
        }
        
    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    def action_open_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'res_model': 'project.task',
            'view_mode': 'form',
            'res_id': self.id,
        }
