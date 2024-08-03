import frappe

@frappe.whitelist()
def get_previous_quantity(water_meter):
    previous_reading = frappe.db.get_value('Meter Reading', {
        'water_meter': water_meter,
    }, 'current_reading', order_by='reading_date desc')
    
    return previous_reading if previous_reading is not None else 0


@frappe.whitelist()
def create_sales_invoice(docname):
    try:
        meter_reading_doc = frappe.get_doc('Meter Reading', docname)
        water_meter_doc = frappe.get_doc('Water Meter', meter_reading_doc.water_meter)

        customer = water_meter_doc.customer

        # Create Sales Invoice
        invoice = frappe.get_doc({
            'doctype': 'Sales Invoice',
            'customer': customer,
            'items': [
                {
                    'item_code': 'Water Consumption',
                    'qty': meter_reading_doc.consumed_quantity,
                    'rate': frappe.db.get_single_value("Water Supply Billing Settings", "cost_per_unit")
                },
                {
                    'item_code': 'Meter Rent',
                    'qty': 1,
                    'rate': frappe.db.get_single_value("Water Supply Billing Settings", "meter_rent")
                },
                {
                    'item_code': 'Water Tax',
                    'qty': 1,
                    'rate': frappe.db.get_single_value("Water Supply Billing Settings", "water_tax")
                }
            ],
            'meter_reading': meter_reading_doc.name
        })

        invoice.insert()

        # Send notification
        send_notification(customer, invoice.name)

        return invoice.name

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'create_sales_invoice Error')
        frappe.throw(f"Error creating Sales Invoice: {str(e)}")

def send_notification(customer, invoice_name):
    # get customer's email
    recipient_email = frappe.db.get_value('Customer', customer, 'email_id')
    subject = f"New Water Bill: {invoice_name}"
    message = f"Dear Customer,\n\nYour new water bill has been generated. Please find the invoice {invoice_name} attached."

    # send email
    frappe.sendmail(recipients=[recipient_email], subject=subject, message=message)
