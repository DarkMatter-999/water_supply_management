frappe.ui.form.on('Meter Reading', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.water_meter) {
            frm.add_custom_button(__('Create Sales Invoice'), function() {
                frappe.call({
                    method: 'utility_billing.api.create_sales_invoice',
                    args: {
                        meter_reading: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Sales Invoice created: {0}', [r.message]));
                        }
                    }
                });
            });
        }
    },
    water_meter: function(frm) {
        if (frm.doc.water_meter) {
            frappe.db.get_value('Meter Reading', {'water_meter': frm.doc.water_meter}, 'current_reading', 'reading_date desc')
            .then(r => {
                if (r.message && r.message.current_reading) {
                    frm.set_value('previous_reading', r.message.current_reading);
                } else {
                    frm.set_value('previous_reading', 0);
                }
            });
        }
    },
    current_reading: function(frm) {
        if (frm.doc.previous_reading != null && frm.doc.current_reading != null) {
            frm.set_value('consumed_quantity', frm.doc.current_reading - frm.doc.previous_reading);
        }
    }
});
