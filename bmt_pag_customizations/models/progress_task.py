# -*- coding: utf-8 -*-
from odoo import models, fields,api,_
#PAG-2-Project-Tasks-Changes
class ProgressTask(models.Model):
    _name = 'progress.task'

    name = fields.Char(string='Name',required=True)
    description = fields.Html(string='Description')
    color = fields.Integer(string='Color')
    
