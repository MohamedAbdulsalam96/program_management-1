# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import (flt)
from frappe.contacts.address_and_contact import load_address_and_contact

class ProjectProposal(Document):
	pass
	def validate(self):
		self.check_percent()

	def check_percent(self):
		total_percent = 0
		for d in self.get("targeted_programs"):
			total_percent += flt(d.percent)

		if flt(total_percent) != 100:
			frappe.throw(_("Sum of percent for all programs should be 100. It is {0}").format(total_percent))
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

@frappe.whitelist()
def make_project(source_name, target_doc=None):
	target_doc = get_mapped_doc("Project Proposal", source_name, {
		"Project Proposal": {
			"doctype": "Project",
			"field_map": {
				"name": "project_proposal",
				"project_title":"project_name",
				"project_no":"project_code",
				"fund_code":"fund_code",
				"planned_start_date":"expected_start_date",
				"planned_end_date":"expected_end_date",
				"budget":"estimated_costing",
			}

		}
	}, target_doc)
	target_doc.from_assessment = "Project Proposal"
	return target_doc