# Copyright (c) 2022, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class XenditChannelData(Document):
	pass


# Dipakai di xendit_channel_data.js
@frappe.whitelist(allow_guest=True)
def calculate(total,xendit_channel_data):
	import math

	doc = frappe.get_doc("Xendit Channel Data",xendit_channel_data)
	total = float(total)
	code = compile(doc.get("fee_calculation"), "<string>", "eval")
	result = eval(code)
	return result
