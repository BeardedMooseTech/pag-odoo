/** @odoo-module **/
//PG-3-Order-of-columns-in-task-list-and-color
import {patch} from "@web/core/utils/patch";
import {ListRenderer} from "@web/views/list/list_renderer";
import {evaluateBooleanExpr} from "@web/core/py_js/py";
patch(ListRenderer.prototype, {
   
    getDynamicColoredStyle(column, record) {
        let style = "";
        let color = this.getDynamicColor(column, record, "bg_color");
        if (color !== undefined) {
            style += `background-color: ${color};`;
        }

        color = this.getDynamicColor(column, record, "fg_color");
        if (color !== undefined) {
            style += `color: ${color};`;
        }

        return style;
    },

    getDynamicColor(column, record, color_target) {
        console.log("getDynamicColor")
        if (color_target in column.options) {
            const definition = column.options[color_target];
            let result = "";
            for (const color_def of definition.split(";")) {
                const color_to_expression = this.pairColorParse(color_def);
                if (color_to_expression !== undefined) {
                    const [color, expression] = color_to_expression;
                    if (
                        evaluateBooleanExpr(
                            expression,
                            record.evalContextWithVirtualIds
                        )
                    ) {
                        result = color;
                    }
                }
            }
            return result || undefined;
        }
    },

    pairColorParse: function (pairColor) {
        if (pairColor !== "") {
            var pairList = pairColor.split(":"),
                color = pairList[0],
                expression = pairList[1] ? pairList[1] : "True";
            return [color, expression];
        }
        return undefined;
    },
});
