import sys
import json
import datetime
from xendit.log import xendit_log

def error_result():
	return sys.exc_info()[1]

def xendit_success(action, response):
	xendit_log(
		action=action,
		type=response.request.method,
		url=response.url,
		payload=response.request.body,
		response=response.content,
		status_code=response.status_code,
		reason=response.reason,
		raw=json.dumps(response.__dict__, default=str)
	)
	data = dict()
	data['code'] = response.status_code
	data['data'] = json.loads(response.content.decode('utf-8'))
	return data

def xendit_error(action, response):
	data = dict()
	if response != None:
		xendit_log(
			action=action,
			type=response.request.method,
			url=response.url,
			payload=response.request.body,
			response=response.content,
			status_code=response.status_code,
			error_type=str(sys.exc_info()[0]),
			error_message=str(sys.exc_info()[1]),
			reason=response.reason,
			raw=json.dumps(response.__dict__, default=str)
		)
		data['code'] = response.status_code
		data['data'] = json.loads(response.content.decode('utf-8'))
	else:
		data['code'] = 500
		data['data'] = "Cannot send request"
	return data