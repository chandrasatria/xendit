import frappe
import json
import string
import sys
from frappe.utils import get_request_session
from xendit.error import *
from xendit.log import *
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_all_payment_method(total):
	from xendit.xendit.doctype.xendit_payment_methods.xendit_payment_methods import calculate
	try:
		category_list = []
		response_category = []
		response = {}
		fga = frappe.get_list("Xendit Payment Methods",fields="*",filters=[["enabled","=",1],["minimal_order","<=",total]],order_by="view_order")
		for item in fga:
			if item["category"] not in category_list:
				response[item["category"]] = []
				image = frappe.get_value("Xendit Payment Category",item["category"],"image")
				response_category.append({"image" : image, "item" : item["category"]})
				category_list.append(item["category"])
				
			item["fee_amount"] = calculate(total, item["name"])
			response[item["category"]].append(item)
		response["availability"] = response_category
		return success_format(response)
	except:
		return error_format(sys.exc_info())
	

@frappe.whitelist(allow_guest=False)
def calculate_payment(total,payment_method_name):
	try:
		from xendit.xendit.doctype.xendit_payment_methods.xendit_payment_methods import calculate
		payment_method_check = frappe.get_value("Xendit Payment Methods",payment_method_name,"name")
		if payment_method_check:
			calculated_total = calculate(total, payment_method_name)
			return success_format(calculated_total)
		else:
			frappe.throw(_("Payment Method not found."))
	except:
		return error_format(sys.exc_info())


