import frappe
import json
import string
from frappe.utils import get_request_session
from xendit.error import *
from xendit.log import *

API_KEY = frappe.get_single("Xendit Setting").api_key
CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token

@frappe.whitelist(allow_guest=False)
def create_disbursement(user, external_doctype, external_id, bank_code, account_holder_name, account_number, description, amount, email_to=[], email_cc=[], email_bcc=[]):
	API_KEY = frappe.get_single("Xendit Setting").api_key
	CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token
	
	import urllib
	request = get_request_session()
	response = None
	url = "https://api.xendit.co/disbursements"
	header = {
		"Authorization": API_KEY,
		"Content-Type": "application/x-www-form-urlencoded"
	}

	payload = "external_id={external_id}&bank_code={bank_code}&account_holder_name={account_holder_name}&account_number={account_number}&description={description}&amount={amount}".format(
		external_id = external_id,
		bank_code = bank_code,
		account_holder_name = account_holder_name,
		account_number = account_number,
		description = description,
		amount = int(amount)
	)

	if len(email_to) > 0:
		payload += "&email_to={email_to}".format(email_to = str(email_to).replace("'", '"'))
		if len(email_cc) > 0:
			payload += "&email_cc={email_cc}".format(email_cc = str(email_cc).replace("'", '"'))
			if len(email_bcc) > 0:
				payload += "&email_bcc={email_bcc}".format(email_bcc = str(email_bcc).replace("'", '"'))

	send_email_to = compile_email_to_html(email_to=email_to, email_cc=email_cc, email_bcc=email_bcc)

	try:
		response = request.post(url=url,headers=header,data=payload,verify=False)
		if response.status_code == 200:
			result = json.loads(response.text)
			doc = frappe.get_doc({
				"doctype": "Xendit Disbursements",
				"docstatus": 1,
				"user": user,
				"user_id": result["user_id"],
				"status" : result["status"],
				"request_on" : frappe.utils.now(),
				"description" : result["disbursement_description"],
				"external_doctype" : external_doctype,
				"external_id" : result["external_id"],
				"bank_code" : result["bank_code"],
				"account_number" : account_number,
				"account_holder_name" : result["account_holder_name"],
				"amount" : int(result["amount"]),
				"request_email_to" : send_email_to,
				"xendit_id" : result["id"],
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			
			xendit_success("Create Disbursements", response)
			return success_format(doc)
		else:
			return xendit_error("Create Disbursements", response)
	except:
		return xendit_error("Create Disbursements", response)

@frappe.whitelist(allow_guest=True)
def callback_disbursement():
	API_KEY = frappe.get_single("Xendit Setting").api_key
	CALLBACK_TOKEN = frappe.get_single("Xendit Setting").callback_token
	
	header_auth = True
	if frappe.request.headers.get("X-Callback-Token") != CALLBACK_TOKEN:
		header_auth = False
	if frappe.request.headers.environ.get("HTTP_X_CALLBACK_TOKEN") != CALLBACK_TOKEN:
		header_auth = False
	if not header_auth:
		return xendit_callback_error("Callback Disbursements", frappe.request, error_type="UNAUTHORIZED_CALLBACK", error_message="Token not match")
	
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		success_email_to = compile_email_to_html(email_to=post.get("email_to", []), email_cc=post.get("email_cc", []), email_bcc=post.get("email_bcc", []))
		xendit_disbursements = frappe.get_all("Xendit Disbursements", fields="name", filters={"xendit_id": post["id"]})
		if len(xendit_disbursements) > 0:
			xd = frappe.get_doc("Xendit Disbursements", xendit_disbursements[0]["name"])
			xd.xendit_id = post.get("id", None)
			xd.user_id = post.get("user_id", None)
			xd.external_id = post.get("external_id", None)
			xd.amount = post.get("amount", None)
			xd.bank_code = post.get("bank_code", None)
			xd.account_holder_name = post.get("account_holder_name", None)
			xd.transaction_id = post.get("transaction_id", None)
			xd.transaction_sequence = post.get("transaction_sequence", None)
			xd.disbursements_id = post.get("disbursements_id", None)
			xd.description = post.get("disbursement_description", None)
			xd.failure_code = post.get("failure_code", None)
			xd.is_instant = post.get("is_instant", None)
			xd.status = post.get("status", None)
			xd.success_email_to = success_email_to
			xd.save(ignore_permissions=True)

			frappe.db.commit()
			return xendit_callback_success("Callback Disbursements", frappe.request)
		else:
			return xendit_callback_error("Callback Disbursements", frappe.request, error_type="MISSING_RESOURCE", error_message="Disbursements not found")
	except:
		return xendit_callback_error("Callback Disbursements", frappe.request)

def compile_email_to_html(email_to, email_cc, email_bcc):
	emails = """
	<table>
	<tr>
		<td>Email To</td>
		<td>:</td>
		<td>{email_to}</td>
	</tr>
	<tr>
		<td>Email CC</td>
		<td>:</td>
		<td>{email_cc}</td>
	</tr>
	<tr>
		<td>Email BCC</td>
		<td>:</td>
		<td>{email_bcc}</td>
	</tr>
	</table>
	""".format(email_to=str(email_to), email_cc=str(email_cc), email_bcc=str(email_bcc))
	return emails