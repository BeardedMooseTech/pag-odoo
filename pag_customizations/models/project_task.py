# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
#PAG-2-Project-Tasks-Changes
class ProjectTask(models.Model):
    _inherit = 'project.task'


    task_status = fields.Many2one('progress.task',string='Status',tracking=True) 
    actual_1 = fields.Char(string="Actual 1",tracking=True)
    actual_2 = fields.Char(string="Actual 2",tracking=True)
    rollup_type = fields.Selection([('1','Avg'),('2','YTD'),('3','Last Actual (Numeric)'),('4','Last Actual (Percentage)')],string="Rollup Type",tracking=True)
    plan_1 = fields.Char(string="Plan 1",tracking=True)
    plan_2 = fields.Char(string="Plan 2",tracking=True)
    status_id = fields.Char(related='task_status.name',string="Status Name")
    #PG-4-Custom-security-on-Planned-fields-on-Progress-tab
    plan_group = fields.Boolean(string="Plan Group",compute="_compute_plan_group")

    def _compute_plan_group(self):
        for rec in self:
            if self.env.user.has_group('pag_customizations.group_user_plans'):
                rec.plan_group = True
            else:
                rec.plan_group = False


    #PG-4-Custom-security-on-Planned-fields-on-Progress-tab
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'list':
            user = self.env.user
            # Condition: Readonly column if the user is NOT in the specific group
            if not user.has_group('pag_customizations.group_user_plans'):
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='plan_2']"):
                    node.set("readonly", "1")
                
        return arch, view