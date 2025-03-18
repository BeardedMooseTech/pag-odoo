# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
#PG-24-Create-Initiative-field-on-the-project-level
class ProjectType(models.Model):
    _name='project.type'
    _description = 'Project Type' 

    name = fields.Char(string='Initiative Name',required=True)
    project_type = fields.Selection([('goals','Goals & Objectives'),('pmo','PMO')],string='Project Type',required=True)

