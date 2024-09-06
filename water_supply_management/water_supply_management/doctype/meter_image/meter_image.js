// Copyright (c) 2024, DarkMatter-999 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meter Image', {
    refresh: function(frm) {
        // Add a custom button to trigger the autofill process and open Meter Reading form
        frm.add_custom_button(__('Autofill and Open Meter Reading'), function() {
            // Call the server-side method to process the image and get the data
            frappe.call({
                method: "water_supply_management.water_supply_management.doctype.meter_image.meter_image.post_image_to_api",
                args: {
                    docname: frm.doc.name
                },
                callback: function(response) {
                    if (response.message) {
                        // Open a new Meter Reading form with the extracted data
                        frappe.model.with_doctype('Meter Reading', function() {
                            var meter_reading = frappe.model.get_new_doc('Meter Reading');
                            meter_reading.water_meter = response.message.water_meter;
                            meter_reading.current_reading = response.message.current_reading;
                            meter_reading.meter_image = frm.doc.name;

                            frappe.set_route('Form', 'Meter Reading', meter_reading.name);
                        });
                    } else {
                        frappe.msgprint(__('Failed to process the image.'));
                    }
                }
            });
        }).addClass('btn-primary');
    }
});