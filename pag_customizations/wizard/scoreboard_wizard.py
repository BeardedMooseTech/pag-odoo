from odoo import models, fields, api

#PG-17-Scorecard-Proof-of-Concept
class ScoreboardWizard(models.TransientModel):
    _name = 'scoreboard.wizard'
    _description = 'Scoreboard Wizard'

    #PG-39-Scorecard-Parent-Task-selection-shows-tasks-from-other-project-types
    #PG-38-Ability-to-print-scorecards-for-more-than-1-parent-task
    task_ids = fields.Many2many('project.task', string="Parent Task",
        domain="[('parent_id', '=', False),('project_type','=','goals')]",
        required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    select_all = fields.Boolean(string="Select All Task")

    @api.onchange('select_all')
    def  onchange_selectall(self):
        for rec in self:
            if rec.select_all:
                rec.task_ids = self.env['project.task'].search([('parent_id', '=', False),('project_type','=','goals')]).ids
            else:
                rec.task_ids = False


    def action_print(self): 
        url = '/download/pdf_zip_from_wizard?ids=%s' % ','.join(map(str, self.ids))
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }