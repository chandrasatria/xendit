import frappe
import json
import sys

def success_format(doc):
	data = dict()
	data['code'] = 200
	data['data'] = doc
	return data

def error_format(exceptions, code = 500, err_text="", indicator = 'red'):
	data = dict()

	if err_text != "":
		data['error'] = err_text
		data['error_type'] = 'ValidationError'
	elif exceptions[0] != None and exceptions[1] != None and exceptions[2] != None:
		if type(exceptions) == str:
			data['error'] = exceptions
			data['error_type'] = 'ValidationError'
		else:
			data['error'] = str(exceptions[1])
			data['error_type'] = type(exceptions[1]).__name__
	else:
		data['error'] = 'ValidationError'
		data['error_type'] = 'ValidationError'

	if exceptions[0] != None and exceptions[1] != None and exceptions[2] != None:
		if type(exceptions) == str:
			data['code'] = code
		else:
			data['code'] = code
			# data['code'] = exceptions[0].http_status_code
	else:
		data['code'] = code
	data['indicator'] = indicator
	return data

def xendit_log(type="",action="",url="",payload="",response="",status_code="",error_type="",error_message="",reason="",raw=""):
	try:
		log = frappe.new_doc("Xendit Log")
		log.type = type
		log.action = action
		log.url = url
		log.payload = payload
		log.response = response
		log.status_code = status_code
		log.error_type = error_type
		log.error_message = error_message
		log.reason = reason
		log.raw = raw
		log.insert(ignore_permissions=True)
		frappe.db.commit()
	except:
		print("TODO: must be write on file log")

def xendit_callback_success(action, request):
	try:
		callback = frappe.new_doc("Xendit Callback")
		callback.action = action
		callback.method = request.method
		callback.url = request.url
		callback.headers = str(request.headers)
		callback.body = request.data
		callback.status = "Success"
		callback.insert(ignore_permissions=True)
		frappe.db.commit()
		return json.loads(request.data)
	except:
		print("TODO: must be write on file log")

def xendit_callback_error(action, request, error_type=None, error_message=None):
	try:
		if not error_type:
			error_type = str(sys.exc_info()[0])
			error_message = str(sys.exc_info()[1])
		callback = frappe.new_doc("Xendit Callback")
		callback.action = action
		callback.method = request.method
		callback.url = request.url
		callback.headers = str(request.headers)
		callback.body = request.data
		callback.status = "Error"
		callback.error_type = error_type
		callback.error_message = error_message
		callback.insert(ignore_permissions=True)
		frappe.db.commit()
		return json.loads(request.data)
	except:
		print("TODO: must be write on file log")