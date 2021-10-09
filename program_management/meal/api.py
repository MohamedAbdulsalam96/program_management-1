# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr, getdate
from frappe.email.doctype.email_group.email_group import add_subscribers

@frappe.whitelist()
def get_project_indicators(project, indicator = None, start_date = None, end_date = None, governorate = None, district = None):
	"""Returns List of Indicator in Project.
	:param project: Project.
	"""	
	condition = ""
	if indicator:
		condition += " AND ind.name = %s " % indicator

	indicators = frappe.db.sql("""select ind_d.name as ind_detail, ind.name as indicator, ind_d.governorate, ind_d.district,
		ind_d.category, ind_d.total, log.name as log, expected_start_date, expected_end_date
		from `tabIndicator Detail` ind_d 
		INNER JOIN `tabIndicators` ind on ind_d.parent=ind.name
		INNER JOIN `tabIndicator Log` log on ind.name=log.indicator
		INNER JOIN `tabProject` pro on ind.project=pro.name
		where ind_d.parenttype='Indicators' and ind.project=%(project)s {condition} order by ind.name asc"""
		.format(condition = condition), {"project": project}, as_dict = True)	


	if not indicators:
		return
	logs = []
	for ind in indicators:
		logs.append(ind['log'])
	log_achiv = frappe.get_all('Achieved Indicators', filters = {'parent': ('in',logs)}, fields = ['total', 'month', 'parent', 'date',
	 'indicator_detail'])

	from dateutil import rrule
	dates = list(rrule.rrule(rrule.MONTHLY, dtstart = (indicators[0]['expected_start_date']).replace(day=1), 
	until = (indicators[0]['expected_end_date']).replace(day=1)))
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	years = {}
	for d in dates:
		years.setdefault(d.year, [])
		years[d.year].append({"month": month[d.month- 1], "date": d})
		
	for ind in indicators:
		ind['years'] = {}
		for year in years:
			ind['years'].setdefault(year, {})
			for month in years[year]:
				ind['years'][year].setdefault(month["month"], 0)
				for achiv in log_achiv:
					frappe.msgprint(frappe.as_json(achiv))
					frappe.msgprint(frappe.as_json(month))
					if achiv['parent'] == ind['log'] and achiv['date'] == month['date'] and achiv['indicator_detail'] == ind['ind_detail']:
						ind['years'][year][month["month"]] = achiv['total']
	return [years, indicators]

@frappe.whitelist()
def get_indicator_by_month(indicator,governorate,district,category,month):
	results = frappe.get_all("Achieved Indicators", filters={"parent": indicator,
		"governorate": governorate, "district": district, "category": category, "month": month, "docstatus": ("!=", 2)})
	if results:
		return frappe.get_doc("Achieved Indicators", results[0])
	else:
		return None

@frappe.whitelist()
def make_indicator_doc(indicators):
	indicators_list = json.loads(indicators)
	for indicator in indicators_list:
		save_achieved(indicator)

def save_achieved(indicator):
	indicator_log = frappe.get_doc("Indicator Log", {"indicator": indicator['indicator']})
	if not indicator_log:
		return

	log_list = frappe.get_all('Achieved Indicators', filters = {"parent": indicator_log.name, 'parenttype': 'Indicator Log',
	'indicator_detail': indicator['ind_detail']}, fields = ['name', 'idx', 'month'])
	
	for month in indicator['months']:
		last_name = None
		for log in log_list:
			if log.month == month:
				last_name = log.name
		if last_name:
			achieved = frappe.get_doc("Achieved Indicators", last_name)
			achieved.update({"total": indicator['months'][month],"parent": indicator_log.name,
				"parenttype": 'Indicator Log',
				"parentfield": "achieved_indicators",
				"idx": (log_list[-1].idx + 1) if log_list else 1,})
			achieved.save()
		else:
			temp = frappe.get_doc("Indicator Detail", indicator['ind_detail'])
			achieved = frappe.get_doc({
				'doctype': 'Achieved Indicators',
				"governorate": temp.governorate,
				"district": temp.district,
				"category": temp.category,
				"type": temp.type,
				"age_group": temp.age_group,
				"men": temp.men,
				"women": temp.women,
				"boys": temp.boys,
				"girls": temp.girls,
				"unclassified": temp.unclassified,
				"hhs": temp.hhs,
				"month": month,
				"total": indicator['months'][month],
				"indicator_detail": indicator['ind_detail'],
				"parent": indicator_log.name,
				"parenttype": 'Indicator Log',
				"parentfield": "achieved_indicators",
				"idx": (log_list[-1].idx + 1) if log_list else 1,
			})
			achieved.insert()