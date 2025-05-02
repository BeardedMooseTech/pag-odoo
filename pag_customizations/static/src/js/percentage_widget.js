/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FloatField } from "@web/views/fields/float/float_field";
import { useInputField } from "@web/views/fields/input_field_hook";

class PercentageField extends FloatField {
    setup() {
        super.setup();
        useInputField({
            getValue: () => this.formattedValue,
            refName: "input",
        });
    }

    
    get formattedValue() {
        const formatted = super.formattedValue;
        if (formatted == null || formatted === "") {
            return formatted;
        }
        if (this.props.record.data.rollup_type === '4') {
            return `${formatted} %`;
        }
        return `${formatted}`;
    }

    parse(value) {
    if (typeof value === "string") {
        value = value.replace(/,/g, "").replace(/\s*%\s*/g, "");
    }
    return parseFloat(value);
}

    getInputProps() {
        const props = super.getInputProps();
        if (this.props.record.data.rollup_type === '4') {
            props.suffix = " %";
        }
        return props;
    }
}

registry.category("fields").add("percentage_field", {
    component: PercentageField,
    supportedTypes: ["float"],
});
