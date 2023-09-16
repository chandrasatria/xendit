import frappe
import json
import string
from frappe.utils import get_request_session
from xendit.error import *
from xendit.log import *
from frappe import _

API_KEY = frappe.get_single("Xendit Setting").api_key
CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token

@frappe.whitelist(allow_guest=False)
def create_invoice(amount, external_doctype, external_id, description="", payment_methods=[],xendit_virtual_account = "", user=None):
	xendit_settings = frappe.get_single("Xendit Setting")

	# MICH: api key dan callback token ga berubah meskipun sudah di ganti di doctype xendit setting, jadi coba aku masukin ke functionnya, bukan sbg global variable (23/12/2020 15:09)
	API_KEY = frappe.get_single("Xendit Setting").api_key
	CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token
	
	import urllib
	
	if user and user != "":
		user = user
	else:
		user = frappe.session.user
	user = frappe.get_doc("User", user)

	request = get_request_session()
	response = None
	url = "https://api.xendit.co/v2/invoices"
	header = {
		"Authorization": API_KEY,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	va_payload = ""
	if xendit_virtual_account:
		va_payload = "&fixed_va=true&callback_virtual_account_id={xendit_virtual_account}".format(xendit_virtual_account = xendit_virtual_account)
		print(xendit_virtual_account)

	payment_method_payload = ""
	if payment_methods:
		payment_method_payload = generate_payment_method_payload(payment_methods,amount)
	
	payload = 'external_id={external_id}&amount={amount}&payer_email={email}&description={description}{payment_method_payload}&should_send_email=true&invoice_duration={invoice_duration}{va_payload}'.format(
		external_id = external_id,
		amount = amount,
		email = user.email,
		description = description,
		payment_method_payload = payment_method_payload,
		payment_methods = '","'.join(payment_methods),
		invoice_duration = xendit_settings.expired_time_in_seconds,
		va_payload = va_payload
	)

	try:
		response = request.post(url=url,headers=header,data=payload,verify=False)
		if response.status_code == 200:
			result = json.loads(response.text)
			doc = frappe.get_doc({
				"doctype": "Xendit Invoice",
				"docstatus": 1,
				"status": result["status"],
				"user": user.name,
				"payer_email": result["payer_email"],
				"should_send_email": False,
				"invoice_url": result["invoice_url"],
				"expiry_date": result["expiry_date"],
				"merchant_name": result["merchant_name"],
				"xendit_id": result["id"],
				"description": result["description"],
				"amount": result['amount'],
				"external_doctype": external_doctype,
				"external_id": external_id
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			
			xendit_success("Create Invoice", response)
			return success_format(doc)
		else:
			return xendit_error("Create Invoice", response)
	except:
		return xendit_error("Create Invoice", response)


def generate_payment_method_payload(payment_methods,amount):
	payment_method_payload = []
	if payment_methods:
		for method in payment_methods:
			if frappe.db.exists("Xendit Payment Methods", method):
				xendit_payment_method = frappe.get_doc("Xendit Payment Methods", method)
				payment_method_payload.append(xendit_payment_method.get("payment_method_value"))
			elif frappe.db.exists("Xendit Payment Methods", {"payment_method_value" : method}):
				xendit_payment_method = frappe.get_doc("Xendit Payment Methods", {"payment_method_value" : method})
				payment_method_payload.append(xendit_payment_method.get("payment_method_value"))
			else:
				frappe.throw(_("""Unable to find Payment Methods."""))
			if amount < xendit_payment_method.minimal_order:
				frappe.throw(_("""Unable to create Xendit Invoice because amount doesn't meet the minimum amount<br>
					Minimum amount of {payment_method} is {minimum_amount}""".format(payment_method=method, minimum_amount=xendit_payment_method.minimal_order)))
			else:
				pass

		payment_method_payload = """&payment_methods=["{payment_methods}"]""" . format(payment_methods = '","'.join(payment_method_payload))
	else:
		payment_method_payload = ""
	return payment_method_payload


@frappe.whitelist(allow_guest=True)
def callback_invoice():
	CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token
	header_auth = True
	if frappe.request.headers.get("X-Callback-Token") != CALLBACK_TOKEN:
		header_auth = False
	if frappe.request.headers.environ.get("HTTP_X_CALLBACK_TOKEN") != CALLBACK_TOKEN:
		header_auth = False
	if not header_auth:
		return xendit_callback_error("Callback Invoice", frappe.request, error_type="UNAUTHORIZED_CALLBACK", error_message="Token not match, token must be {}".format(CALLBACK_TOKEN))
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		xendit_invoice = frappe.get_all("Xendit Invoice", fields="*", filters={"xendit_id": post["id"]})
		if len(xendit_invoice) > 0:
			xi = frappe.get_doc("Xendit Invoice", xendit_invoice[0]["name"])
			xi.status = post["status"]
			xi.payment_method = post.get("payment_method", None)
			xi.payment_channel = post.get("payment_channel", None)
			xi.payment_destination = post.get("payment_destination", None)
			xi.credit_card_charge_id = post.get("credit_card_charge_id", None)
			xi.paid_at = frappe.utils.now()
			xi.fees_paid_amount = post.get("fees_paid_amount", None)
			xi.adjusted_received_amount = post.get("adjusted_received_amount", None)
			xi.bank_code = post.get("bank_code", None)
			xi.merchant_name = post.get("merchant_name", None)
			xi.retail_outlet_name = post.get("retail_outlet_name", None)
			xi.paid_amount = post.get("paid_amount", None)
			xi.save(ignore_permissions=True)

			frappe.db.commit()
			return xendit_callback_success("Callback Invoice", frappe.request)
		else:
			return xendit_callback_error("Callback Invoice", frappe.request, error_type="MISSING_RESOURCE", error_message="Invoice not found")
	except:
		return xendit_callback_error("Callback Invoice", frappe.request)

@frappe.whitelist(allow_guest=False)
def get_invoice(invoice):
	xendit_id = frappe.get_value("Xendit Invoice", {"name": invoice}, "xendit_id")
	if xendit_id:
		request = get_request_session()
		response = None
		url = "https://api.xendit.co/v2/invoices/" + xendit_id
		header = {
			"Authorization": API_KEY
		}
		try:
			response = request.get(url=url,headers=header,verify=False)
			if response.status_code == 200:
				return xendit_success("Get Invoice", response)
			else:
				return xendit_error("Get Invoice", response)
		except:
			return xendit_error("Get Invoice", response)
	else:
		return frappe.throw("Invoice not found")

def make_invoice_expired(xendit_invoice):
	xendit_invoice = frappe.get_doc("Xendit Invoice", xendit_invoice)
	if xendit_invoice.status == "PENDING":
		response = None

		request = get_request_session()
		url = "https://api.xendit.co/invoices/{xendit_id}/expire!".format(xendit_id = xendit_invoice.xendit_id)
		header = {
			"Authorization": API_KEY
		}
		try:
			response = request.post(url=url, headers=header, verify=False)
			if response.status_code == 200:
				result = json.loads(response.text)
				xendit_invoice.status = result.get("status", None)
				xendit_invoice.expired_on = frappe.utils.now()
				xendit_invoice.save(ignore_permissions=True)
				frappe.db.commit()

				return xendit_success("Make Invoice Expired", response)
			else:
				return xendit_error("Make Invoice Expired", response)
		except:
			return xendit_error("Make Invoice Expired", response)
	else:
		frappe.throw(_("Invalid Xendit Invoice Status"))
