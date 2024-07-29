import frappe

def create_sales_invoice(self, event):
    meter_reading_doc = self
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
                'rate': 10  # Eg Fixed rate per unit
            },
            {
                'item_code': 'Meter Rent',
                'qty': 1,
                'rate': 5  # Eg meter rent
            },
            {
                'item_code': 'Water Tax',
                'qty': 1,
                'rate': 2  # Eg water tax
            }
        ],
        'meter_reading': meter_reading_doc.name
    })

    invoice.insert()
    invoice.submit()

    # Send notification
    send_notification(customer, invoice.name)

def send_notification(customer, invoice_name):
    # get customer's email
    recipient_email = frappe.db.get_value('Customer', customer, 'email_id')
    subject = f"New Water Bill: {invoice_name}"
    message = f"Dear Customer,\n\nYour new water bill has been generated. Please find the invoice {invoice_name} attached."

    # send email
    frappe.sendmail(recipients=[recipient_email], subject=subject, message=message)
