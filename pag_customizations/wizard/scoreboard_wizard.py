from odoo import models, fields, api

#PG-17-Scorecard-Proof-of-Concept
class ScoreboardWizard(models.TransientModel):
    _name = 'scoreboard.wizard'
    _description = 'Scoreboard Wizard'

    #PG-39-Scorecard-Parent-Task-selection-shows-tasks-from-other-project-types
    task = fields.Many2one(
        'project.task',
        string="Parent Task",
        domain="[('parent_id', '=', False),('project_type','=','goals')]",
        required=True
    )

    child_task_ids = fields.One2many(
        'project.task',
        'wizard_id',
        string="Child Tasks",
        compute='_compute_child_tasks',
        store=False
    )
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    

    @api.depends('task')
    def _compute_child_tasks(self):
        for wizard in self:
            print("wizard",wizard,wizard.task)
            if wizard.task:
                wizard.child_task_ids = self.env['project.task'].search([
                    ('parent_id', '=', wizard.task.id)
                ])
            else:
                wizard.child_task_ids = []

    def action_print(self): 
        return self.env.ref('pag_customizations.action_pag_scoreboard_report').report_action(self)
