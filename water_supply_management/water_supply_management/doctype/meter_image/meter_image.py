# Copyright (c) 2024, DarkMatter-999 and contributors
# For license information, please see license.txt

import frappe
import requests
import json

from frappe.model.document import Document
from frappe.utils.file_manager import get_file

@frappe.whitelist()
def post_image_to_api(docname):
	doc = frappe.get_doc("Meter Image", docname)

	api_url = frappe.db.get_single_value('Water Supply Billing Settings', 'image_api')
	
	if not api_url:
		frappe.throw("Please configure the Image API host in Water Supply Billing Settings.")

	if not doc.meter_image:
		frappe.throw("Please attach an image to the Meter Reading.")

	file_doc = frappe.get_doc("File", {"file_url": doc.meter_image})
	file_path = file_doc.get_full_path()

	with open(file_path, 'rb') as image_file:
		image_data = image_file.read()

	# Send the image file to the external API
	try:
		response = requests.post(
			url=api_url,
			files={'image': image_data}
		)

		data = json.loads(response.text)
		
		water_meter = data["meter_no"]
		current_reading = float(data["meter_reading"])
		
		extracted_data = {"water_meter": water_meter, "current_reading": current_reading}

		if response.status_code == 200:
			return extracted_data

		else:
			frappe.throw(f"Failed to submit image: {response.text}")

	except Exception as e:
		frappe.throw(f"Error submitting image to API: {str(e)}")


class MeterImage(Document):
	pass
