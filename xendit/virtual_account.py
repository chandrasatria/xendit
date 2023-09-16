import frappe
import json
import string
from frappe.utils import get_request_session
from xendit.error import *
from xendit.log import *

API_KEY = frappe.get_single("Xendit Setting").api_key
CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token

@frappe.whitelist(allow_guest=False)
def available_bank():
	request = get_request_session()
	url = "https://api.xendit.co/available_virtual_account_banks"
	header = {
		"Authorization": API_KEY
	}
	res = request.get(url=url,headers=header,verify=False)
	data = res.json()
	return data

@frappe.whitelist(allow_guest=False)
def create_virtual_account(user, bank):
	user = frappe.get_doc("User", frappe.session.user)
	request = get_request_session()
	response = None
	url = "https://api.xendit.co/callback_virtual_accounts"
	header = {
		"Authorization": API_KEY,
		"Content-Type": "application/json"
	}
	data = {
	   "external_id": user.name,
	   "bank_code": bank,
	   "name": user.first_name
	}
	try:
		response = request.post(url=url,headers=header,data=json.dumps(data),verify=False)
		if response.status_code == 200:
			result = json.loads(response.text)
			doc = frappe.get_doc({
				"doctype": "Xendit Virtual Account",
				"docstatus": 0,
				"status": result["status"],
				"user": result["external_id"],
				"account_number": result["account_number"],
				"bank_code": result["bank_code"],
				"xendit_id": result["id"],
				"xendit_owner_id": result['owner_id']
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()

			xendit_success("Create FVA", response)
			return success_format(doc)
		else:
			return xendit_error("Create FVA", response)
	except:
		return xendit_error("Create FVA", response)

@frappe.whitelist(allow_guest=True)
def callback_virtual_accounts():
	header_auth = True
	if frappe.request.headers.get("X-Callback-Token") != CALLBACK_TOKEN:
		header_auth = False
	if frappe.request.headers.environ.get("HTTP_X_CALLBACK_TOKEN") != CALLBACK_TOKEN:
		header_auth = False
	if not header_auth:
		return xendit_callback_error("Callback Create FVA", frappe.request, error_type="UNAUTHORIZED_CALLBACK", error_message="Token not match")
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		xendit_virtual_account = frappe.get_all("Xendit Virtual Account", fields="*", filters={"user": post["external_id"], "account_number": post["account_number"], "bank_code": post["bank_code"]})
		print(xendit_virtual_account)
		if len(xendit_virtual_account) > 0:
			xva = frappe.get_doc("Xendit Virtual Account", xendit_virtual_account[0]["name"])
			xva.xendit_id = post["id"]
			xva.status = post["status"]
			xva.save(ignore_permissions=True)
			frappe.db.commit()
			return xendit_callback_success("Callback Create FVA", frappe.request)
		else:
			return xendit_callback_error("Callback Create FVA", frappe.request, error_type="Virtual Account not found")
	except:
		return xendit_callback_error("Callback Create FVA", frappe.request)

@frappe.whitelist(allow_guest=False)
def get_virtual_account(account_number):
	xendit_id = frappe.get_value("Xendit Virtual Account", {"account_number": account_number}, "xendit_id")
	if xendit_id:
		request = get_request_session()
		response = None
		url = "https://api.xendit.co/callback_virtual_accounts/{}".format(xendit_id)
		# url = "https://api.xendit.co/callback_virtual_accounts/id=" + xendit_id
		header = {
			"Authorization": API_KEY
		}
		try:
			response = request.get(url=url,headers=header , verify=False)
			if response.status_code == 200:
				return xendit_success("Get FVA Detail", response)
			else:
				return xendit_error("Get FVA Detail", response)
		except:
			return xendit_error("Get FVA Detail", response)
	else:
		return frappe.throw("Account Number not found")