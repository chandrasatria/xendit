import frappe
import json
import string
from frappe.utils import get_request_session
from error import *
from log import *

API_KEY = frappe.get_single("Xendit Setting").api_key
CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token

@frappe.whitelist(allow_guest=False)
def create_payment(amount, phone, ewallet_type, external_doctype, external_id):
	user = frappe.get_doc("User", frappe.session.user)
	request = get_request_session()
	response = None
	url = "https://api.xendit.co/ewallets"
	header = {
		"Authorization": API_KEY,
		"Content-Type": "application/json"
	}
	data = {
	    "external_id": external_id,
	    "amount": amount,
	    "phone": phone,
	    "ewallet_type": ewallet_type
	}
	try:
		response = request.post(url=url,headers=header,data=json.dumps(data),verify=False)
		if response.status_code == 200:
			result = json.loads(response.text)
			doc = frappe.get_doc({
				"doctype": "Xendit eWallet",
				"docstatus": 1,
				"status": result["status"],
				"user": frappe.session.user,
				"payer_email": frappe.session.user,
				"phone": result["phone"],
				"created_on": frappe.utils.now(),
				"external_doctype": external_doctype,
				"external_id": external_id,
				"ewallet_type": result["ewallet_type"],
				"amount": result["amount"],
				"business_id": result["business_id"]
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			
			xendit_success("E-Wallet Payment", response)
			return success_format(doc)
		else:
			return xendit_error("E-Wallet Payment", response)
	except:
		return xendit_error("E-Wallet Payment", response)

@frappe.whitelist(allow_guest=True)
def callback_ewallet():
	if frappe.request.headers.get("X-Callback-Token") != CALLBACK_TOKEN:
		return xendit_callback_error("Callback eWallet", frappe.request, error_type="UNAUTHORIZED_CALLBACK", error_message="Token not match")
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		xendit_ewallet = frappe.get_all("Xendit eWallet", fields="*", filters={"external_id": post["external_id"]})
		if len(xendit_ewallet) > 0:
			xew = frappe.get_doc("Xendit eWallet", xendit_ewallet[0]["name"])
			xew.status = post.get("status", None)
			xew.paid_amount = post.get("amount", None)
			xew.paid_on = frappe.utils.now()
			xew.failure_code = post.get("failure_code", None)
			xew.save(ignore_permissions=True)

			frappe.db.commit()
			return xendit_callback_success("Callback eWallet", frappe.request)
		else:
			return xendit_callback_error("Callback eWallet", frappe.request, error_type="MISSING_RESOURCE", error_message="eWallet not found")
	except:
		return xendit_callback_error("Callback eWallet", frappe.request)

@frappe.whitelist(allow_guest=False)
def get_ewallet(external_id, ewallet_type):
	xendit_ewallet = frappe.get_value("Xendit eWallet", {"external_id": external_id}, "external_id")
	if xendit_ewallet:
		request = get_request_session()
		response = None
		url = "https://api.xendit.co/ewallets?external_id=" + external_id + "&ewallet_type=" + ewallet_type
		header = {
			"Authorization": API_KEY
		}
		try:
			response = request.get(url=url,headers=header,verify=False)
			if response.status_code == 200:
				return xendit_success("Get eWallet", response)
			else:
				return xendit_error("Get eWallet", response)
		except:
			return xendit_error("Get eWallet", response)
	else:
		return frappe.throw("eWallet not found")