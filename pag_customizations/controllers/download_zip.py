from odoo import http
from odoo.http import request
import io
import zipfile
from odoo.exceptions import UserError
#PG-38-Ability-to-print-scorecards-for-more-than-1-parent-task
class ScoreboardDownloadController(http.Controller):

    @http.route('/download/pdf_zip_from_wizard', type='http', auth='user')
    def download_pdf_zip_from_wizard(self, ids=None, **kwargs):
        if not ids:
            return request.not_found()

        ids_list = [int(x) for x in ids.split(',')]
        records = request.env['scoreboard.wizard'].browse(ids_list)
        zip_buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)
        report_action = request.env.ref('pag_customizations.action_pag_scoreboard_report')
        try:
            for index, record in enumerate(records, start=1):
                for task  in record.task_ids:
                    try:
                        pdf_content, _ = report_action._render_qweb_pdf(report_action.id,record.ids, data={'task': task})
                    except Exception as e:
                        raise UserError(f"Failed to generate PDF for Scorecard {index}: {str(task.name)}")
                   
                    base_name = task.name.replace(' ', '_')
                    filename = f"{base_name}.pdf"
                    zip_file.writestr(filename, pdf_content)
            zip_file.close()
            zip_buffer.seek(0)
            zip_data = zip_buffer.read()
        except UserError as error:
        # Close zip and buffer properly
            zip_file.close()
            zip_buffer.close()
            raise UserError(error)


        return request.make_response(
            zip_data,
            headers=[
                ('Content-Type', 'application/zip'),
                ('Content-Disposition', 'attachment; filename="scoreboard_reports.zip"')
            ]
        )
