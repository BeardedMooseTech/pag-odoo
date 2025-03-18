# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
#PG-24-Create-Initiative-field-on-the-project-level
class ProjectProject(models.Model):
    _inherit = 'project.project'

    initiative_id = fields.Many2one('project.type',string='Initiative',required=True)
    project_type = fields.Selection([('goals','Goals & Objectives'),('pmo','PMO')],string='Project Type',required=True)
    
    @api.onchange('initiative_id')
    def onchange_project_initative(self):
        for rec in self:
            if rec.initiative_id:
                rec.project_type = rec.initiative_id.project_type


    
