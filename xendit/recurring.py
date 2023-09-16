import frappe
from frappe import _

# lib
import json
import requests
from xendit.error import xendit_error, xendit_success
from xendit.log import success_format

"""
from xendit.recurring import deactive
a = deactive(
	plan_id="repl_d0d48ed0-8bc0-40cc-9e30-20e23944f18b"
)
print(a)

from xendit.recurring import create_plan
a = create_plan(
	reference_id="reference_id_1",
	customer_xendit_id="cust-e6e0da37-72e2-41ec-ba8b-c0fbba8580f2",
	recurring_action="PAYMENT",
	currency="IDR",
	amount=2800000,
	interval="MONTH",
	interval_count=1,
	success_return_url="https://dev.openthedoor.co.id/",
	failure_return_url="https://dev.openthedoor.co.id/"
)
print(a)

from xendit.recurring import get_cycles_list
a = get_cycles_list(
	plan_id="repl_5758abea-1c2a-4a1b-b012-8dad5ba504e0"
)
print(a)

from xendit.recurring import simulate_status
a = simulate_status(
	plan_id="repl_5758abea-1c2a-4a1b-b012-8dad5ba504e0",
	cycle_id="recy_ec98e687-b63f-495f-8805-951268757e9e"
)
print(a)

from xendit.recurring import update_plan
a = update_plan(
	plan_id="repl_5758abea-1c2a-4a1b-b012-8dad5ba504e0",
	update_scheduled_cycle=True,
	amount=1500000
)
print(a)

from xendit.recurring import update_schedule
a = update_schedule(
	schedule_id="resc_1f24575b-ec3a-424e-ad31-935a455609a6",
	update_scheduled_cycle=True,
	interval="MONTH",
	interval_count=2
)
print(a)
"""

def update_schedule(schedule_id, update_scheduled_cycle=None, interval=None, interval_count=None, total_recurrence=None, anchor_date=None, retry_interval=None, retry_interval_count=None, total_retry=None, failed_attempt_notifications=None):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	nama_log = "Recurring Update Schedule"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/schedules/{0}".format(schedule_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {}

	# cek parameter untuk header, perlu diupdate?
	if update_scheduled_cycle == True:
		# ya
		headers.update({
			"update-scheduled-cycle"		: str(update_scheduled_cycle)
		})
	else:
		# tidak
		pass

	# cek parameter untuk body, perlu diupdate?
	if interval is None or interval == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"interval"		: interval
		})
	
	if interval_count is None or interval_count == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"interval_count"		: interval_count
		})
	
	if total_recurrence is None or total_recurrence == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"total_recurrence"		: total_recurrence
		})
	
	if anchor_date is None or anchor_date == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"anchor_date"		: anchor_date
		})
	
	if retry_interval is None or retry_interval == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"retry_interval"		: retry_interval
		})
	
	if retry_interval_count is None or retry_interval_count == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"retry_interval_count"		: retry_interval_count
		})
	
	if total_retry is None or total_retry == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"total_retry"		: total_retry
		})
	
	if failed_attempt_notifications is None or failed_attempt_notifications == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"failed_attempt_notifications"		: failed_attempt_notifications
		})

	# variabel
	response = None

	try:
		# request
		response = requests.request(
			method="PATCH",
			url=url,
			headers=headers,
			json=payload
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(nama_log)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(nama_log, response)

	# buat xendit log
	xendit_success(nama_log, response)

	# convert
	response_json = json.loads(res_text)

	# response
	return success_format(response_json)

def update_plan(plan_id, update_scheduled_cycle=None, customer_id=None, currency=None, amount=None, payment_methods=None, recurring_created=None, recurring_succeeded=None, recurring_failed=None, locale=None, metadata=None, description=None, items=None):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	log_name = "Recurring Update Plan"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/plans/{0}".format(plan_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {}

	# cek parameter untuk header, perlu diupdate?
	if update_scheduled_cycle == True:
		# ya
		headers.update({
			"update-scheduled-cycle"		: str(update_scheduled_cycle)
		})
	else:
		# tidak
		pass
	
	# cek parameter untuk body, perlu diupdate?
	if customer_id is None or customer_id == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"customer_id"		: customer_id
		})

	if currency is None or currency == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"currency"		: currency
		})
	
	if amount is None or amount == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"amount"		: amount
		})
	
	if payment_methods is None or payment_methods == "" or payment_methods == []:
		# tidak
		pass
	else:
		# ya
		payload.update({
			"payment_methods"		: payment_methods
		})
	
	if recurring_created is None or recurring_created == "" or recurring_succeeded is None or recurring_succeeded == "" or recurring_failed is None or recurring_failed == "" or locale is None or locale == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"notification_config"		: {
				"recurring_created"			: recurring_created,
				"recurring_succeeded"		: recurring_succeeded,
				"recurring_failed"			: recurring_failed,
				"locale"					: locale
			}
		})
	
	if metadata is None or metadata == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"metadata"		: metadata
		})
	
	if description is None or description == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"description"		: description
		})
	
	if items is None or items == "" or items == []:
		# tidak
		pass
	else:
		# ya
		payload.update({
			"items"		: items
		})

	# variabel
	response = None

	try:
		# request
		response = requests.request(
			method="PATCH",
			url=url,
			headers=headers,
			json=payload
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(log_name)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(log_name, response)

	# buat xendit log
	xendit_success(log_name, response)

	# convert
	response_json = json.loads(res_text)

	# response
	return success_format(response_json)

def simulate_status(plan_id, cycle_id):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	nama_log = "Recurring Simulate Status"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/plans/{0}/cycles/{1}/simulate".format(plan_id, cycle_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	
	# amount hardcode karena merupakan `Magic Number`
	payload = {
		"amount"		: int(13579)
	}

	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="POST",
			url=url,
			headers=headers,
			json=payload
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(nama_log)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(nama_log, response)

	# buat xendit log
	xendit_success(nama_log, response)

	# convert
	response_json = json.loads(res_text)

	# response
	return success_format(response_json)

def get_cycles_list(plan_id, limit=None, after_id=None):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	nama_log = "Recurring Get Cycles List"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/plans/{0}/cycles".format(plan_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {}
	
	# cek parameter ada?
	if limit is None or limit == "" or limit == 0:
		# tidak
		pass
	else:
		# ya
		payload.update({
			"limit"		: limit
		})
		
	if after_id is None or after_id == "" or after_id == 0:
		# tidak
		pass
	else:
		# ya
		payload.update({
			"after_id"		: after_id
		})

	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="GET",
			url=url,
			headers=headers,
			json=payload
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(nama_log)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(nama_log, response)

	# buat xendit log
	xendit_success(nama_log, response)

	# convert
	response_json = json.loads(res_text)

	# response
	return success_format(response_json)

def deactive(plan_id):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	nama_log = "Recurring Deactive"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/plans/{0}/deactivate".format(plan_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}

	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="POST",
			url=url,
			headers=headers
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(nama_log)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(nama_log, response)

	# buat xendit log
	xendit_success(nama_log, response)

	# convert
	response_json = json.loads(res_text)

	# cari dokumen
	xendit_recurring_plan_id_list = frappe.db.sql_list("""
		SELECT
			name
		FROM `tabXendit Recurring Plan`
		WHERE
			plan_id = %(plan_id)s
	""", {
		"plan_id"		: plan_id
	})

	# cek ada xendit customer?
	xendit_recurring_plan_doc_list = []
	if len(xendit_recurring_plan_id_list) <= 0:
		# tidak ada
		pass
	else:
		# ada
		for xendit_recurring_plan_id in xendit_recurring_plan_id_list:
			# ambil doc
			xendit_recurring_plan_doc = frappe.get_doc("Xendit Recurring Plan", xendit_recurring_plan_id)

			# append
			xendit_recurring_plan_doc_list.append(xendit_recurring_plan_doc)

	# looping
	for xendit_recurring_plan_doc in xendit_recurring_plan_doc_list:
		# update
		xendit_recurring_plan_doc.update({
			"status"			: "Inactive"
		})

		# simpan
		xendit_recurring_plan_doc.save(ignore_permissions=True)

	# commit
	frappe.db.commit()

	# response
	return success_format(response_json)

def create_plan(reference_id, customer_xendit_id, recurring_action, currency, amount, schedule_id=None, interval=None, interval_count=None, total_recurrence=None, anchor_date=None, retry_interval=None, retry_interval_count=None, total_retry=None, failed_attempt_notifications=None, payment_methods=None, immediate_action_type=None, recurring_created=None, recurring_succeeded=None, recurring_failed=None, locale=None, failed_cycle_action=None, metadata=None, description=None, items=None, actions=None, success_return_url=None, failure_return_url=None):
	# ambil xendit settings doc
	xendit_settings_doc = frappe.get_single("Xendit Setting")

	# ambil variabel yang dibutuhkan
	xendit_settings_doc_api_key = getattr(xendit_settings_doc, "api_key", None)

	# cek variabel lengkap?
	if xendit_settings_doc_api_key is None or xendit_settings_doc_api_key == "":
		# tidak
		return
	else:
		# ya
		pass

	# variabel log
	nama_log = "Recurring Create Plan"

	# variabel kebutuhan request
	url = "https://api.xendit.co/recurring/plans"
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}

	# payload
	payload = {
		"reference_id"				: reference_id,
		"customer_id"				: customer_xendit_id,
		"recurring_action"			: recurring_action,
		"currency"					: currency,
		"amount"					: amount
	}

	# validasi variabel
	schedule_reference_id = reference_id

	# tambah dengan parameter yang ada isinya
	# parameter schedule
	if schedule_id is None or schedule_id == "":
		# buat baru
		payload_schedule = {
			"reference_id"			: schedule_reference_id,
			"interval"				: interval,
			"interval_count"		: interval_count
		}

		# cek parameter ada?
		if total_recurrence is None or total_recurrence == "":
			# tidak
			pass
		else:
			# ya
			payload_schedule.update({
				"total_recurrence"		: total_recurrence,
			})
		
		if anchor_date is None or anchor_date == "":
			# tidak
			pass
		else:
			# ada
			payload_schedule.update({
				"anchor_date"			: anchor_date,
			})
		
		if retry_interval is None or retry_interval == "":
			# tidak
			pass
		else:
			# ada
			payload_schedule.update({
				"retry_interval"				: retry_interval,
			})
		
		if retry_interval_count is None or retry_interval_count == "":
			# tidak
			pass
		else:
			# ada
			payload_schedule.update({
				"retry_interval_count"			: retry_interval_count,
			})
		
		if total_retry is None or total_retry == "":
			# tidak
			pass
		else:
			# ada
			payload_schedule.update({
				"total_retry"					: total_retry,
			})
		
		if failed_attempt_notifications is None or failed_attempt_notifications == "":
			# tidak
			pass
		else:
			# ada
			payload_schedule.update({
				"failed_attempt_notifications"			: failed_attempt_notifications,
			})
		
		# update
		payload.update({
			"schedule"		: payload_schedule
		})
	else:
		# pake schedule yang sudah ada
		payload.update({
			"schedule_id"	: schedule_id
		})
	
	# cek notification config
	if recurring_created is None or recurring_created == "" or recurring_succeeded is None or recurring_succeeded == "" or recurring_failed is None or recurring_failed == "" or locale is None or locale == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"recurring_created"			: recurring_created,
			"recurring_succeeded"		: recurring_succeeded,
			"recurring_failed"			: recurring_failed,
			"locale"					: locale
		})

	# parameter lainnya
	if payment_methods is None or payment_methods == "" or payment_methods == []:
		# tidak
		pass
	else:
		# ada
		payload.update({
			"payment_methods"			: payment_methods
		})

	if immediate_action_type is None or immediate_action_type == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"immediate_action_type"			: immediate_action_type
		})
	
	if failed_cycle_action is None or failed_cycle_action == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"failed_cycle_action"			: failed_cycle_action
		})
	
	if metadata is None or metadata == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"metadata"			: metadata
		})
	
	if description is None or description == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"description"			: description
		})
	
	if items is None or items == "" or items == []:
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"items"			: items
		})
	
	if actions is None or actions == "" or actions == []:
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"actions"			: actions
		})
	
	if success_return_url is None or success_return_url == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"success_return_url"			: success_return_url
		})
	
	if failure_return_url is None or failure_return_url == "":
		# tidak
		pass
	else:
		# ya
		# ada
		payload.update({
			"failure_return_url"			: failure_return_url
		})
	
	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="POST",
			url=url,
			headers=headers,
			json=payload,
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit {0}".format(nama_log)))
		return

	# ambil variabel yang dibutuhkan
	res_status_code = response.status_code
	res_text = response.text

	# cek berhasil?
	if res_status_code >= 200 and res_status_code < 300:
		# ya
		pass
	else:
		# tidak
		return xendit_error(nama_log, response)

	# buat xendit log
	xendit_success(nama_log, response)

	# convert
	response_json = json.loads(res_text)

	"""response
	{
		"reference_id": "reference_id_1",
		"customer_id": "cust-e6e0da37-72e2-41ec-ba8b-c0fbba8580f2",
		"recurring_action": "PAYMENT",
		"currency": "IDR",
		"amount": 2800000,
		"success_return_url": "https://dev.openthedoor.co.id/",
		"failure_return_url": "https://dev.openthedoor.co.id/",
		"schedule_id": "resc_b3aad1d7-35a2-469a-87cf-044a6abe89bd",
		"status": "REQUIRES_ACTION",
		"immediate_action_type": None,
		"metadata": None,
		"description": None,
		"items": None,
		"id": "repl_5d1e8ecf-1b59-4845-ac51-6888b03ff370",
		"created": "2023-03-10T05:21:58.484Z",
		"updated": "2023-03-10T05:21:58.484Z",
		"payment_methods": [],
		"notification_config": {
			"locale": "en"
		},
		"failed_cycle_action": "RESUME",
		"payment_link_for_failed_attempt": False,
		"schedule": {
			"reference_id": "reference_id_1",
			"interval": "MONTH",
			"interval_count": 2,
			"business_id": "5f645ac6e1d07e792ca3dd3c",
			"anchor_date": "2023-03-10T05:21:58.485Z",
			"total_recurrence": None,
			"retry_interval": None,
			"retry_interval_count": None,
			"total_retry": None,
			"id": "resc_b3aad1d7-35a2-469a-87cf-044a6abe89bd",
			"failed_attempt_notifications": [],
			"created": "2023-03-10T05:21:58.484Z",
			"updated": "2023-03-10T05:21:58.484Z"
		},
		"actions": [
			{
				"action": "AUTH",
				"url": "https://linking-dev.xendit.co/pali_f466c276-7cc5-49b6-8059-5582b4aa232e",
				"url_type": "WEB",
				"method": "GET"
			}
		],
		"recurring_cycle_count": 0
	}
	"""

	# ambil variabel yang dibutuhkan
	response_json_id = response_json.get("id", None)
	response_json_reference_id = response_json.get("reference_id", None)
	response_json_customer_id = response_json.get("customer_id", None)
	response_json_schedule_id = response_json.get("schedule_id", None)
	response_json_actions = response_json.get("actions", None)

	# cek actions
	response_json_url = None
	if response_json_actions is None or response_json_actions == "" or response_json_actions == []:
		# tidak
		pass
	else:
		# ada
		response_json_url = response_json_actions[0].get("url", None)

	# buat dokumen
	xendit_recurring_plan_doc = frappe.new_doc("Xendit Recurring Plan")

	# update
	xendit_recurring_plan_doc.update({
		"status"				: "Active",
		"plan_id"				: response_json_id,
		"reference_id"			: response_json_reference_id,
		"customer_id"			: response_json_customer_id,
		"schedule_id"			: response_json_schedule_id,
		"url"					: response_json_url
	})

	# simpan
	xendit_recurring_plan_doc.save(ignore_permissions=True)

	# commit
	frappe.db.commit()

	# response
	return success_format(response_json)