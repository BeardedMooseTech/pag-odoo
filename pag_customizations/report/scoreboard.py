import logging
from odoo import models, api
from datetime import datetime

_logger = logging.getLogger(__name__)
#PG-17-Scorecard-Proof-of-Concept
class ScoreboardReport(models.AbstractModel):
    _name = "report.pag_customizations.report_pag_scoreboard"
    _description = "Pag Scoreboard Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Fetch parent tasks and all nested subtasks, then pass them to the report."""

        all_tasks = self.env["project.task"].search([])
        parent_tasks = all_tasks.filtered(lambda t: not t.parent_id)  # Fetch only parent tasks
        if not parent_tasks:
            return {"parent_tasks": []}

        month_fields = {
            1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
            7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec"
        }

        def fetch_subtasks(task):
            """Recursively fetch all subtasks and sum their plan & actual values."""
            subtasks = self.env["project.task"].search([("parent_id", "=", task.id)])

            plan_total = 0.0
            actual_total = 0.0
            subtask_list = []

            for sub in subtasks:
                nested_plan_total, nested_actual_total = fetch_subtasks(sub)
                total_plan = sub.plan_1 + nested_plan_total
                total_actual = sub.actual_1 + nested_actual_total

                plan_total += total_plan
                actual_total += total_actual

            return plan_total, actual_total

        report_values = []
        for task in parent_tasks:
            owner_name = task.user_ids[0].name if task.user_ids else "Unassigned"
            task_plan_total =0
            task_actual_total = 0
            months_data = {m: {"plan": 0.0, "actual": 0.0} for m in month_fields.values()}

            plan_total, actual_total = fetch_subtasks(task)

            task_plan_total =  plan_total
            task_actual_total = actual_total

            task_month_str = ""
            if task.date_assign:
                task_month = task.date_assign.month
                task_month_str = month_fields.get(task_month, "")

            if task_month_str:
                months_data[task_month_str]["plan"] = "{:.2f}".format(float(task_plan_total))
                months_data[task_month_str]["actual"] = "{:.2f}".format(float(task_actual_total))
               
            report_values.append({
                "task_name": task.name,
                "owner": owner_name,
                "months_data": months_data,
            })
        return {
            "doc_ids": parent_tasks.ids,
            "doc_model": "project.task",
            "parent_tasks": report_values,
        }