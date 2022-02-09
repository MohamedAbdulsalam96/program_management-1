# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import month_diff
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
				"planned_start_date":"expected_start_date",
				"planned_end_date":"expected_end_date",
				"project_budget_usd":"estimated_costing",
			}

		}
	}, target_doc)
	target_doc.from_assessment = "Project Proposal"
	return target_doc


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_governorate(doctype, txt, searchfield, start, page_len, filters):
	if not filters: filters = {}
	condition = ""
	if filters.get("parent"):
		if filters.get("type"):
			if filters.get("type")=="Project":
				filters["parent"] = frappe.get_value("Project", filters.get("parent"), "project_proposal")
		condition += "and parent = %(parent)s"
	
	return frappe.db.sql("""select governorate from `tabGovernorates`
				where `governorate` LIKE %(txt)s
				{condition} 
			order by idx desc, name"""
			.format(condition=condition), {
				'txt': '%' + txt + '%',
				'parent': filters.get("parent", "")
			})


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_district(doctype, txt, searchfield, start, page_len, filters):
	if not filters: filters = {}
	condition = ""
	if filters.get("parent"):
		condition += "and parent = %(parent)s"
	
	return frappe.db.sql("""select district from `tabDistricts`
				where `district` LIKE %(txt)s
				{condition} 
			order by idx desc, name"""
			.format(condition=condition), {
				'txt': '%' + txt + '%',
				'parent': filters.get("parent", "")
			})

@frappe.whitelist()
def get_governorate_district(parent):
	res = {}
	res['governorate'] =  frappe.db.sql("""select governorate from `tabGovernorates`
		where parent = %(parent)s
		order by idx desc, name""", {'parent': parent})
	res['district'] =  frappe.db.sql("""select district from `tabDistricts`
		where parent = %(parent)s
		order by idx desc, name""", {'parent': parent})
	return res