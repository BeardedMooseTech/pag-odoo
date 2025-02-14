# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
from lxml import etree
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
                for node in arch.iterfind(".//field[@name='child_ids']/list/field[@name='plan_2']"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='plan_2']"):
                    node.set("readonly", "1")
                    
                res['views']['form']['arch'] = etree.tostring(arch, encoding='unicode')
        if res['views'].get('list'):
            arch = res['views']['list']['arch']
            user = self.env.user
            if not user.has_group('pag_customizations.group_user_plans'):
                arch = etree.fromstring(arch)  
                for node in arch.iterfind(".//field[@name='plan_1']"):
                    node.set("readonly", "1")
                for node in arch.iterfind(".//field[@name='plan_2']"):
                    node.set("readonly", "1")

                res['views']['list']['arch'] = etree.tostring(arch, encoding='unicode')
        return res

    