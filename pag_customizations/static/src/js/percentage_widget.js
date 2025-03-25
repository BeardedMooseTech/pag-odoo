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

    // Format the display value (readonly mode)
    get formattedValue() {
        const formatted = super.formattedValue;
        if (formatted == null || formatted === "") {
            return formatted;
        }
        const num = parseFloat(formatted);
        if (this.props.record.data.rollup_type === '4') {
            return `${num} %`;  // % appears after the number in readonly
        }
        return formatted;
    }

    // Parse the input value (ensure % does not affect saving)
    parse(value) {
        if (typeof value === "string") {
            value = value.replace(/\s*%\s*/g, ""); // Remove % if manually typed
        }
        return super.parse(value);
    }

    // Render the input field with a % suffix (edit mode)
    getInputProps() {
        const props = super.getInputProps();
        if (this.props.record.data.rollup_type === '4') {
            // Add a suffix outside the input (Odoo 18 supports this)
            props.suffix = " %";
        }
        return props;
    }
}

registry.category("fields").add("percentage_field", {
    component: PercentageField,
    supportedTypes: ["float"],
});