# Copyright (c) 2024, DarkMatter-999 and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document

class MeterReading(Document):
    def before_save(self):
        self.calculate_consumed_quantity()

    def calculate_consumed_quantity(self):
        if self.water_meter:
            previous_reading = frappe.db.get_value('Meter Reading', {
                'water_meter': self.water_meter,
                'name': ('!=', self.name)
            }, 'current_reading', order_by='reading_date desc')
            
            self.previous_reading = previous_reading if previous_reading is not None else 0
            
            if self.previous_reading is not None and self.current_reading is not None:
                self.consumed_quantity = self.current_reading - self.previous_reading
            else:
                self.consumed_quantity = 0
                