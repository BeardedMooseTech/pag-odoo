/** @odoo-module **/
import { ProjectTaskFormController } from "@project/views/project_task_form/project_task_form_controller";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
//PG-5-Default-tab-view-on-the-task
patch(ProjectTaskFormController.prototype,{

    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems();
        setTimeout(() => {
            let notebookTabs =  document.querySelectorAll('.o_notebook_headers .nav-item');
            let targetTab = false;
            if (notebookTabs && notebookTabs.length>2) {
                let subtaskField = document.querySelector(".o_field_widget[name='subtask_count']");
                let hasSubtasks = subtaskField && subtaskField.innerText.trim() !== "";
                if (hasSubtasks){
                    let tab = document.querySelector('.o_notebook_headers .nav-item:nth-child(2) a');
                    targetTab = tab;
                }
                else{
                    let progressTabs = document.querySelector('.o_notebook_headers .nav-item:nth-child(3) a');
                    targetTab = progressTabs;
                }
                if (targetTab) {
                    targetTab.click();
                }
            }
            else{
                let progressTabs = document.querySelector('.o_notebook_headers .nav-item:nth-child(2) a');
                targetTab = progressTabs;
                if (targetTab) {
                    targetTab.click();
                }
            }
        }, 500); // Delay to ensure form is rendered
       return menuItems;
    }
});
