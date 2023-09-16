# -*- coding: utf-8 -*-
# Copyright (c) 2019, digitalasiasolusindo@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


frappe.flags.xendit_basic
frappe.flags.xendit_virtual_account

def create_xendit_basic():
	if frappe.flags.xendit_basic:
		return
	from xendit.invoice import create_invoice
	response = create_invoice(10000,"Xendit Log","XLog-000011",description="test.py")
	frappe.flags.xendit_basic = response

def create_xendit_with_virtual_account():
	if frappe.flags.xendit_virtual_account:
		return
	from xendit.invoice import create_invoice
	response = create_invoice(10000,"Xendit Log","XLog-000011",description="test.py",xendit_virtual_account = "5fbf29a7e993697b4c2f8fbd")
	print(response)
	frappe.flags.xendit_basic = response

def create_xendit_with_virtual_account_with_payment_method():
	if frappe.flags.xendit_virtual_account:
		return
	from xendit.invoice import create_invoice
	response = create_invoice(10000,"Xendit Log","XLog-000011",description="test.py",payment_methods=["BCA"],xendit_virtual_account = "5fbf29a7e993697b4c2f8fbd")
	print(response)
	frappe.flags.xendit_basic = response

class TestXenditInvoice(unittest.TestCase):
	def setUp(self):
		create_xendit_basic()

	def test_create_xendit_basic(self):
		# root = frappe.get_doc('Entitas', 'root')
		
		# return OK status if and only if the new entitas has root as parent
		# and root entitas still has empty parent
		print(frappe.flags.xendit_basic)
		self.assertTrue(not frappe.flags.xendit_basic)