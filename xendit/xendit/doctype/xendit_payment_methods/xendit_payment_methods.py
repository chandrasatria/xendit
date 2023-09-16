# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from math import *

class XenditPaymentMethods(Document):
	pass


# Dipakai di xendit_payment_methods.js
@frappe.whitelist(allow_guest=True)
def calculate(total,xendit_payment_methods):
	import math

	doc = frappe.get_doc("Xendit Payment Methods",xendit_payment_methods)
	total = float(total)
	code = compile(doc.get("fee_calculation"), "<string>", "eval")
	result = eval(code)
	return result

