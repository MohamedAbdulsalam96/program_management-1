# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Indicators(Document):
	def validate(self):
		if self.is_percentage==1 and self.is_cumulative==1:
			frappe.throw("Should be on of these (Is Percentage, Is Cumulative), not all")
		self.calc_indicator_detail()
		
	def calc_indicator_detail(self):
		last_ind=0
		for ind in self.indicator_detail:
			if last_ind==0:
				last_ind=ind.total
			if last_ind!=ind.total and self.is_cumulative==1:
				frappe.throw("The indicator is cumulative, so all total in details should be same")			
			last_ind=ind.total
			self.total=ind.total
	

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_governorate(doctype, txt, searchfield, start, page_len, filters):
	if not filters: filters = {}
	condition = ""
	if filters.get("parent"):
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
