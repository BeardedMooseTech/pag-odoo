/** @odoo-module **/
//PG-5-Default-tab-view-on-the-task
import { ProjectTaskFormController } from "@project/views/project_task_form/project_task_form_controller";
import { patch } from "@web/core/utils/patch";
patch(ProjectTaskFormController.prototype,{
    setup() {
        super.setup(); 
        setTimeout(() => {
            let notebookTabs =  document.querySelector('.o_notebook_headers .nav-item:nth-child(2) a');
            let subtaskField = document.querySelector(".o_field_widget[name='subtask_count']");
            if (notebookTabs) {
                let hasSubtasks = subtaskField && subtaskField.innerText.trim() !== "";
                let tab = document.querySelector('.o_notebook_headers .nav-item:nth-child(2) a');
                let progressTabs = document.querySelector('.o_notebook_headers .nav-item:nth-child(4) a');
                let targetTab = hasSubtasks ? tab : progressTabs;
                if (targetTab) {
                    targetTab.click();
                }
            }
        }, 500); // Delay to ensure form is rendered
    }
});
