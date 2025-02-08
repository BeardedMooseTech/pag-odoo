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