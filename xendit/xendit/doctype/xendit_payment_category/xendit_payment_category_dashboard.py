from frappe import _

def get_data():
	return {
		'fieldname': 'category',
		'transactions': [
			{
				'label': _('Xendit Payment Method'),
				'items': ['Xendit Payment Method']
			}
		]
	}