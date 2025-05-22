# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
from lxml import etree
from odoo.exceptions import AccessError,UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime

#PAG-2-Project-Tasks-Changes
class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = "name asc"


    task_status = fields.Many2one('progress.task',string='Status',tracking=True) 
    #PG-43-Remove-decimal-places-from-Scorecard
    actual_1 = fields.Float(string="Actual",tracking=True,digits=(16, 0))
    actual_2 = fields.Float(string="Actual 2",tracking=True)
    # PG-22-View-as-if-based-metric
    plan_1 = fields.Float(string="Plan",tracking=True,digits=(16, 0))
    #PG-18-Make-Roll-up-Type-not-required-on-parent-level
    rollup_type = fields.Selection([('1','Avg'),('2','YTD'),('3','Last Actual (Numeric)'),('4','Last Actual (Percentage)')],string="Rollup Type",tracking=True)
    plan_2 = fields.Float(string="Plan 2",tracking=True)
    status_id = fields.Char(related='task_status.name',string="Status Name")
    #PG-24-Create-Initiative-field-on-the-project-level
    initiative_id = fields.Many2one('project.type',related='project_id.initiative_id',string='Initiative',store=True)
    project_type = fields.Selection(related='project_id.project_type',string='Project Type',store=True)
    #PG-30-Unable-to-create-a-Task-in-the-Projects-module
    wizard_id = fields.Many2one('project.task',string="Wizard ID")
    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    related_tasks = fields.Many2many(
    'project.task',
    'project_task_related_task_rel',  
    'task_id',                        
    'related_task_id', 
    string='Related Tasks')
    task_id = fields.Many2one('project.task', string='Tasks', readonly=True)
    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    parent_task_id = fields.Many2one('project.task', string='Parent Task' ,domain=[('parent_id','=',False)])
    #PG-34-Gray-out-Planned-values-for-months-in-the-future-based-on-date
    task_date = fields.Date(string="Date")

    @api.model
    def sync_existing_parent_id(self):
        tasks = self.search([('parent_id','=',False)])
        for task in tasks:
            for task in task.child_ids:
                task.parent_task_id = task.parent_id.id if task.parent_id else False
            


    @api.model_create_multi
    def create(self, vals_list):
        task = super().create(vals_list)
        #PG-16-Tasks-and-Sub-tasks-Expanded-View
        for vals in vals_list:
            if vals.get('child_ids'):
                task._sync_child_ids_to_m2m()
                task._sync_m2m_to_child_ids()
            if 'rollup_type' in vals:
                for task in self:
                    task._add_rollup_type_to_subtask(vals['rollup_type'])
        return task

   
    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    def _sync_child_ids_to_m2m(self):
        for task in self:
            task.related_tasks = [(6, 0, task.child_ids.ids)]

    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    def _sync_m2m_to_child_ids(self):
        for task in self:
            for subtask in task.related_tasks:
                if subtask.parent_id.id != task.id:
                    subtask.parent_id = task

    #PG-16-Tasks-and-Sub-tasks-Expanded-View
    @api.model
    def sync_existing_subtasks_to_m2m(self):
        tasks = self.search([])
        for task in tasks:
            task.related_tasks = [(6, 0, task.child_ids.ids)]
            for subtask in task.related_tasks:
                if subtask.parent_id.id != task.id:
                    subtask.parent_id = task

 
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
                for node in arch.xpath("//field"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='task_status']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='actual_1']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='rollup_type']"):
                    node.set("readonly", "0")

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
                for node in arch.xpath("//field"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='task_status']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='actual_1']"):
                    node.set("readonly", "0")
                for node in arch.iterfind(".//field[@name='rollup_type']"):
                    node.set("readonly", "0")

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
                continue

            sub_tasks = task.child_ids.filtered(lambda t: not t.child_ids)
            if not sub_tasks:
                continue

            # Compute last month
            last_month = datetime.today() - relativedelta(months=1)
            last_month_str = last_month.strftime('%b %Y')

            sub_tasks_last_month = sub_tasks.filtered(
                lambda t: t.name and last_month_str in t.name
            )

            if task.rollup_type == '1':
                if sub_tasks_last_month and sub_tasks_last_month.actual_1:
                    task.actual_1 = sum(sub_tasks_last_month.mapped('actual_1')) / len(sub_tasks_last_month)
              
            elif task.rollup_type == '2' and sub_tasks_last_month.actual_1:
                if sub_tasks_last_month:
                    task.actual_1 = sum(sub_tasks_last_month.mapped('actual_1'))
                

            elif task.rollup_type in ('3', '4') and sub_tasks_last_month.actual_1:
                latest_task = sub_tasks_last_month.sorted(lambda t: t.write_date, reverse=True)[:1]
                if latest_task:
                    task.actual_1 = latest_task.actual_1 or 0.0

            # Set parent status based on most recently updated subtask
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
            #PG-33-Odoo-Server-Savepoint-Error-when-importing-data-on-sub-sub-task
            try:
                with self.env.cr.savepoint():
                    if self.project_type =='goals':
                    # Trigger parent update after saving sub-task changes
                        for task in tasks_to_update:
                            if task.parent_id:
                                task.parent_id._compute_roll_up_values()
            except UserError as e:
                _logger.info(e)
        if 'rollup_type' in vals:
            for task in self:
                task._add_rollup_type_to_subtask(vals['rollup_type'])
        #PG-16-Tasks-and-Sub-tasks-Expanded-View
        if vals.get('child_ids'):
            self._sync_child_ids_to_m2m()
            self._sync_m2m_to_child_ids()
        return result

    #PG-52-Final-Changes-and-Feedback
    def _add_rollup_type_to_subtask(self, rollup_type):
        for child in self.child_ids:
            child.rollup_type = rollup_type
            child._add_rollup_type_to_subtask(rollup_type)

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

    #PG-21-Permissions-change
    def hide_record_rule(self):
        rule_id= self.env['ir.rule'].search([('active','=',True),('name','in',['Project: See private tasks','Project: Portal User Restriction','Project: portal users: portal and following','Project: employees: following required for follower-only projects','Project/Task: employees: follow required for follower-only projects'])])
        if rule_id:
            rule_id.sudo().write({'active':False})
        return True
        