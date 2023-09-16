import frappe
from frappe import _

# lib
import json
import requests
from xendit.error import xendit_error, xendit_success
from xendit.log import success_format

def update_customer(reference_doctype, reference_id, xendit_id, type, api_version=None, given_names=None, surname=None, nationality=None, place_of_birth=None, date_of_birth=None, gender=None, employer_name=None, employer_nature_of_business=None, role_description=None, business_name=None, trading_name=None, business_type=None, nature_of_business=None, business_domicile=None, date_of_registration=None, mobile_number=None, phone_number=None, email=None, addresses=None, identity_accounts=None, kyc_documents=None, description=None, domicile_of_registration=None, metadata=None):
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

	# variabel kebutuhan request
	url = "https://api.xendit.co/customers/{0}".format(xendit_id)
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {}

	# cek parameter tambahan untuk header
	if api_version is None or api_version == "":
		# tidak
		pass
	else:
		# ya
		headers.update({
			"API-VERSION"			: api_version
		})

	# cek parameter untuk body
	# set berdasarkan api version
	if api_version == "2020-10-31":
		# cek tipe
		# sesuai dengan yang di sarankan xendit (2023/03)
		if type == "INDIVIDUAL":
			# variabel
			individual_detail = {
				"given_names"				: given_names
			}

			# cek parameter ada?
			if surname is None or surname == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"surname"			: surname
				})
			
			if nationality is None or nationality == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"nationality"			: nationality
				})

			if place_of_birth is None or place_of_birth == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"place_of_birth"			: place_of_birth
				})
			
			if date_of_birth is None or date_of_birth == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"date_of_birth"			: date_of_birth
				})
			
			if gender is None or gender == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"gender"			: gender
				})
			
			if employer_name is None or employer_name == "" or employer_nature_of_business is None or employer_nature_of_business == "" or role_description is None or role_description == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"employment"			: {
						"employer_name"				: employer_name,
						"nature_of_business"		: employer_nature_of_business,
						"role_description"			: role_description
					}
				})

			# update
			payload.update({
				"individual_detail"		: individual_detail
			})
		elif type == "BUSINESS":
			# variabel
			business_detail = {
				"business_name"				: business_name,
				"business_type"				: business_type
			}

			# cek parameter ada?
			if trading_name is None or trading_name == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"trading_name"				: trading_name
				})
				
			if nature_of_business is None or nature_of_business == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"nature_of_business"		: nature_of_business
				})
			
			if business_domicile is None or business_domicile == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"business_domicile"			: business_domicile
				})
			
			if date_of_registration is None or date_of_registration == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"date_of_registration"			: date_of_registration
				})
			
			# update
			payload.update({
				"business_detail"		: business_detail
			})
		else:
			# selain itu
			return
	else:
		# parameter individual
		if given_names is None or given_names == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"given_names"			: given_names
			})

		if surname is None or surname == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"surname"			: surname
			})
		
		if nationality is None or nationality == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"nationality"			: nationality
			})

		if place_of_birth is None or place_of_birth == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"place_of_birth"			: place_of_birth
			})
		
		if date_of_birth is None or date_of_birth == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"date_of_birth"			: date_of_birth
			})
		
		if gender is None or gender == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"gender"			: gender
			})

		if employer_name is None or employer_name == "" or employer_nature_of_business is None or employer_nature_of_business == "" or role_description is None or role_description == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"employment"			: {
					"employer_name"					: employer_name,
					"nature_of_business"			: employer_nature_of_business,
					"role_description"				: role_description
				}
			})
		
		# parameter business
		if business_name is None or business_name == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_name"				: business_name
			})
		
		if business_type is None or business_type == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_type"				: business_type
			})
		
		if trading_name is None or trading_name == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"trading_name"				: trading_name
			})
		
		if nature_of_business is None or nature_of_business == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"nature_of_business"		: nature_of_business
			})
		
		if business_domicile is None or business_domicile == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_domicile"			: business_domicile
			})
		
		if date_of_registration is None or date_of_registration == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"date_of_registration"			: date_of_registration
			})
		
	# parameter lainnya
	if mobile_number is None or mobile_number == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"mobile_number"				: mobile_number
		})

	if phone_number is None or phone_number == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"phone_number"				: phone_number
		})
	
	if email is None or email == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"email"				: email
		})
	
	if addresses is None or addresses == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"addresses"				: addresses
		})
	
	if identity_accounts is None or identity_accounts == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"identity_accounts"				: identity_accounts
		})
	
	if kyc_documents is None or kyc_documents == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"kyc_documents"				: kyc_documents
		})
	
	if description is None or description == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"description"				: description
		})

	if date_of_registration is None or date_of_registration == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"date_of_registration"				: date_of_registration
		})

	if domicile_of_registration is None or domicile_of_registration == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"domicile_of_registration"				: domicile_of_registration
		})

	if metadata is None or metadata == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"metadata"				: metadata
		})

	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="PATCH",
			url=url,
			headers=headers,
			json=payload,
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit Update Customer"))
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
		return xendit_error("Update Customer", response)

	# buat xendit log
	xendit_success("Update Customer", response)

	# convert
	response_json = json.loads(res_text)

	# ambil variabel yang dibutuhkan
	response_json_id = response_json.get("id", None)
	response_json_reference_id = response_json.get("reference_id", None)
	response_json_type = response_json.get("type", None)
	response_json_individual_detail = response_json.get("individual_detail", None)
	response_json_business_detail = response_json.get("business_detail", None)
	response_json_email = response_json.get("email", None)
	response_json_mobile_number = response_json.get("mobile_number", None)
	response_json_phone_number = response_json.get("phone_number", None)
	response_json_hashed_phone_number = response_json.get("hashed_phone_number", None)
	response_json_addresses = response_json.get("addresses", None)
	response_json_identity_accounts = response_json.get("identity_accounts", None)
	response_json_kyc_documents = response_json.get("kyc_documents", None)
	response_json_description = response_json.get("description", None)
	response_json_date_of_registration = response_json.get("date_of_registration", None)
	response_json_domicile_of_registration = response_json.get("domicile_of_registration", None)
	response_json_metadata = response_json.get("metadata", None)
	response_json_created = response_json.get("created", None)
	response_json_updated = response_json.get("updated", None)

	# cari dokumen
	xendit_customer_id_list = frappe.db.sql_list("""
		SELECT
			name
		FROM `tabXendit Customer`
		WHERE
			xendit_id = %(xendit_id)s
	""", {
		"xendit_id"		: response_json_id
	})

	# cek ada xendit customer?
	xendit_customer_doc_list = []
	if len(xendit_customer_id_list) <= 0:
		# tidak ada
		# buat dokumen
		xendit_customer_doc = frappe.new_doc("Xendit Customer")

		# append
		xendit_customer_doc_list.append(xendit_customer_doc)
	else:
		# ada
		for xendit_customer_id in xendit_customer_id_list:
			# ambil doc
			xendit_customer_doc = frappe.get_doc("Xendit Customer", xendit_customer_id)

			# append
			xendit_customer_doc_list.append(xendit_customer_doc)

	# looping
	for xendit_customer_doc in xendit_customer_doc_list:
		# update
		xendit_customer_doc.update({
			"xendit_id"						: response_json_id,
			"email"							: response_json_email,
			"reference_doctype"				: reference_doctype,
			"reference_id"					: response_json_reference_id
		})

		# simpan
		xendit_customer_doc.save(ignore_permissions=True)

	# commit
	frappe.db.commit()

	# response
	return success_format(xendit_customer_doc)

def get_customer_by_reference_id(reference_id):
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

	# variabel kebutuhan request
	url = "https://api.xendit.co/customers"
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {
		"reference_id"		: reference_id
	}

	# variabel
	response = None
	try:
		# request
		response = requests.request(
			method="GET",
			url=url,
			headers=headers,
			params=payload
		)
	except:
		# gagal
		frappe.log_error(frappe.get_traceback(), _("ERROR: Xendit Get Customer by Reference ID"))
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
		return xendit_error("Get Customer by Reference ID", response)

	# buat xendit log
	xendit_success("Get Customer by Reference ID", response)

	# convert
	response_json = json.loads(res_text)

	# response
	return success_format(response_json)

def create_customer(reference_doctype, reference_id, type, api_version=None, given_names=None, surname=None, nationality=None, place_of_birth=None, date_of_birth=None, gender=None, employer_name=None, employer_nature_of_business=None, role_description=None, business_name=None, trading_name=None, business_type=None, nature_of_business=None, business_domicile=None, date_of_registration=None, mobile_number=None, phone_number=None, hashed_phone_number=None, email=None, addresses=None, identity_accounts=None, kyc_documents=None, description=None, domicile_of_registration=None, metadata=None):
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
	nama_log = "Create Customer"

	# variabel kebutuhan request
	url = "https://api.xendit.co/customers"
	headers = {
		"Authorization"		: xendit_settings_doc_api_key
	}
	payload = {
		"reference_id"				: reference_id,
		"type"						: type
	}

	# cek parameter tambahan untuk header
	if api_version is None or api_version == "":
		# tidak
		pass
	else:
		# ya
		headers.update({
			"API-VERSION"			: api_version
		})

	# cek parameter untuk body
	# set berdasarkan api version
	if api_version == "2020-10-31":
		# cek tipe
		# sesuai dengan yang di sarankan xendit (2023/03)
		if type == "INDIVIDUAL":
			# variabel
			individual_detail = {
				"given_names"				: given_names
			}

			# cek parameter ada?
			if surname is None or surname == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"surname"			: surname
				})
			
			if nationality is None or nationality == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"nationality"			: nationality
				})

			if place_of_birth is None or place_of_birth == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"place_of_birth"			: place_of_birth
				})
			
			if date_of_birth is None or date_of_birth == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"date_of_birth"			: date_of_birth
				})
			
			if gender is None or gender == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"gender"			: gender
				})
			
			if employer_name is None or employer_name == "" or employer_nature_of_business is None or employer_nature_of_business == "" or role_description is None or role_description == "":
				# tidak
				pass
			else:
				# ya
				individual_detail.update({
					"employment"			: {
						"employer_name"				: employer_name,
						"nature_of_business"		: employer_nature_of_business,
						"role_description"			: role_description
					}
				})

			# update
			payload.update({
				"individual_detail"		: individual_detail
			})
		elif type == "BUSINESS":
			# variabel
			business_detail = {
				"business_name"				: business_name,
				"business_type"				: business_type
			}

			# cek parameter ada?
			if trading_name is None or trading_name == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"trading_name"				: trading_name
				})
				
			if nature_of_business is None or nature_of_business == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"nature_of_business"		: nature_of_business
				})
			
			if business_domicile is None or business_domicile == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"business_domicile"			: business_domicile
				})
			
			if date_of_registration is None or date_of_registration == "":
				# tidak
				pass
			else:
				# ya
				business_detail.update({
					"date_of_registration"			: date_of_registration
				})
			
			# update
			payload.update({
				"business_detail"		: business_detail
			})
		else:
			# selain itu
			return
	else:
		# parameter individual
		if given_names is None or given_names == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"given_names"			: given_names
			})

		if surname is None or surname == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"surname"			: surname
			})
		
		if nationality is None or nationality == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"nationality"			: nationality
			})

		if place_of_birth is None or place_of_birth == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"place_of_birth"			: place_of_birth
			})
		
		if date_of_birth is None or date_of_birth == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"date_of_birth"			: date_of_birth
			})
		
		if gender is None or gender == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"gender"			: gender
			})

		if employer_name is None or employer_name == "" or employer_nature_of_business is None or employer_nature_of_business == "" or role_description is None or role_description == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"employment"			: {
					"employer_name"					: employer_name,
					"nature_of_business"			: employer_nature_of_business,
					"role_description"				: role_description
				}
			})
		
		# parameter business
		if business_name is None or business_name == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_name"				: business_name
			})
		
		if business_type is None or business_type == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_type"				: business_type
			})
		
		if trading_name is None or trading_name == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"trading_name"				: trading_name
			})
		
		if nature_of_business is None or nature_of_business == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"nature_of_business"		: nature_of_business
			})
		
		if business_domicile is None or business_domicile == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"business_domicile"			: business_domicile
			})
		
		if date_of_registration is None or date_of_registration == "":
			# tidak
			pass
		else:
			# ya
			payload.update({
				"date_of_registration"			: date_of_registration
			})
		
	# parameter lainnya
	if mobile_number is None or mobile_number == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"mobile_number"				: mobile_number
		})

	if phone_number is None or phone_number == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"phone_number"				: phone_number
		})

	if hashed_phone_number is None or hashed_phone_number == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"hashed_phone_number"				: hashed_phone_number
		})
	
	if email is None or email == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"email"				: email
		})
	
	if addresses is None or addresses == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"addresses"				: addresses
		})
	
	if identity_accounts is None or identity_accounts == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"identity_accounts"				: identity_accounts
		})
	
	if kyc_documents is None or kyc_documents == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"kyc_documents"				: kyc_documents
		})
	
	if description is None or description == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"description"				: description
		})

	if date_of_registration is None or date_of_registration == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"date_of_registration"				: date_of_registration
		})

	if domicile_of_registration is None or domicile_of_registration == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"domicile_of_registration"				: domicile_of_registration
		})

	if metadata is None or metadata == "":
		# tidak
		pass
	else:
		# ya
		payload.update({
			"metadata"				: metadata
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

	# ambil variabel yang dibutuhkan
	response_json_id = response_json.get("id", None)
	response_json_reference_id = response_json.get("reference_id", None)
	response_json_type = response_json.get("type", None)
	response_json_individual_detail = response_json.get("individual_detail", None)
	response_json_business_detail = response_json.get("business_detail", None)
	response_json_email = response_json.get("email", None)
	response_json_mobile_number = response_json.get("mobile_number", None)
	response_json_phone_number = response_json.get("phone_number", None)
	response_json_hashed_phone_number = response_json.get("hashed_phone_number", None)
	response_json_addresses = response_json.get("addresses", None)
	response_json_identity_accounts = response_json.get("identity_accounts", None)
	response_json_kyc_documents = response_json.get("kyc_documents", None)
	response_json_description = response_json.get("description", None)
	response_json_date_of_registration = response_json.get("date_of_registration", None)
	response_json_domicile_of_registration = response_json.get("domicile_of_registration", None)
	response_json_metadata = response_json.get("metadata", None)
	response_json_created = response_json.get("created", None)
	response_json_updated = response_json.get("updated", None)

	# buat dokumen
	xendit_customer_doc = frappe.new_doc("Xendit Customer")

	# update
	xendit_customer_doc.update({
		"xendit_id"						: response_json_id,
		"email"							: response_json_email,
		"reference_doctype"				: reference_doctype,
		"reference_id"					: response_json_reference_id
	})

	# simpan
	xendit_customer_doc.save(ignore_permissions=True)

	# commit
	frappe.db.commit()

	# response
	return success_format(xendit_customer_doc)