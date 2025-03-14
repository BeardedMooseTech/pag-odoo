/** @odoo-module **/
import { ProjectTaskFormController } from "@project/views/project_task_form/project_task_form_controller";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
//PG-5-Default-tab-view-on-the-task
patch(ProjectTaskFormController.prototype,{

     setup() {
        super.setup();
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
                    let progressTab = document.querySelector('.o_notebook_headers .nav-item:nth-child(3) a');
                    let notebookName = progressTab?.textContent.trim();
                    if (notebookName === "Progress") {  
                        targetTab = progressTab;
                    } 
                    else {
                        targetTab = document.querySelector('.o_notebook_headers .nav-item:nth-child(4) a');
                        }
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
    },

    async onPagerUpdate({ offset, resIds }) {
        super.onPagerUpdate(...arguments);
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
                    let progressTab = document.querySelector('.o_notebook_headers .nav-item:nth-child(3) a');
                    let notebookName = progressTab?.textContent.trim();
                    if (notebookName === "Progress") {  
                        targetTab = progressTab;
                    } 
                    else {
                        targetTab = document.querySelector('.o_notebook_headers .nav-item:nth-child(4) a');
                        }
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
    }
});
