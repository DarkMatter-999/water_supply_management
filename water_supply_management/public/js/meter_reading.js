frappe.ui.form.on('Meter Reading', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.water_meter && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Sales Invoice'), function() {
                frappe.call({
                    method: 'water_supply_management.api.create_sales_invoice',
                    args: {
                        docname: frm.doc.name,
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Sales Invoice created: {0}', [r.message]));

                            // Redirect to the newly created Sales Invoice
                            frappe.set_route('Form', 'Sales Invoice', r.message);
                        }
                    }
                });
            });
        } else {
            frm.remove_custom_button(__('Create Sales Invoice'));
        }
    },
    water_meter: function(frm) {
        if (frm.doc.water_meter) {
            frappe.call({
                method: 'water_supply_management.api.get_previous_quantity',
                args: {
                    water_meter: frm.doc.water_meter,
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('previous_reading', r.message);
                    } else {
                        frm.set_value('previous_reading', 0);
                    }

                    // Calculate consumed quantity if current reading is already set
                    if (frm.doc.current_reading != null) {
                        frm.set_value('consumed_quantity', frm.doc.current_reading - frm.doc.previous_reading);
                    }
                }
            });
        }
    },
    current_reading: function(frm) {
        // Check if current reading is less than previous reading
        if (frm.doc.previous_reading && frm.doc.current_reading < frm.doc.previous_reading) {
            frappe.msgprint(__("Current reading cannot be less than previous reading."));
            frm.set_value('current_reading', frm.doc.previous_reading); // Reset to previous reading
            return;
        }

        if (frm.doc.previous_reading != null && frm.doc.current_reading != null) {
            frm.set_value('consumed_quantity', frm.doc.current_reading - frm.doc.previous_reading);
        }
    },
    before_save: function(frm) {
        // Ensure consumed quantity is calculated before saving
        if (frm.doc.previous_reading != null && frm.doc.current_reading != null) {
            frm.set_value('consumed_quantity', frm.doc.current_reading - frm.doc.previous_reading);
        }
    }
});
