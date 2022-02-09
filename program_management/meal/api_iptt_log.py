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
		condition += " AND ind.name = '%s' " % indicator
	if start_date and end_date:
		condition += " AND  pro.expected_start_date >= '%s' and  pro.expected_end_date <= '%s'" % (start_date, end_date)
	if governorate:
		condition += " AND ind_d.governorate = '%s' " % governorate.replace("'", "")
	if district:
		condition += " AND ind_d.district = '%s' " %  district.replace("'", "")

	indicators = frappe.db.sql("""select ind.code, log.indicator_subject, ind_d.name as ind_detail, ind.name as indicator, ind_d.is_unclassified,
		ind_d.men, ind_d.women, ind_d.boys, ind_d.girls, ind_d.governorate, ind_d.district, ind_d.category, ind_d.total, 
		log.name as log, pro.expected_start_date, pro.expected_end_date
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
	log_achiv = frappe.get_all('Achieved Indicators', filters = {'parent': ('in',logs)}, fields = ['men', 'women', 'boys', 'girls',
	'total', 'month', 'parent', 'date', 'indicator_detail'])

	from dateutil import rrule
	dates = list(rrule.rrule(rrule.MONTHLY, dtstart = (indicators[0]['expected_start_date']).replace(day=1), 
	until = (indicators[0]['expected_end_date']).replace(day=1)))
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	years = {}
	for d in dates:
		years.setdefault(d.year, [])
		date = frappe.utils.getdate(d)
		years[d.year].append({"month": month[d.month- 1], "date": date})
	
	# for ind in indicators:
	# 	ind['months'] = {}
	# 	for year in years:
	# 		for month in years[year]:
	# 			ind['months'].setdefault(cstr(month['date']), 0)
	# 			for achiv in log_achiv:
	# 				if achiv['parent'] == ind['log'] and achiv['date'] == month['date'] and achiv['indicator_detail'] == ind['ind_detail']:
	# 					ind['months'][cstr(month["date"])] = achiv['total']

	result = {}
	for ind in indicators:
		ind['months'] = {}
		ind['gender'] = []
		if ind.is_unclassified == 0:
			if ind.men > 0:
				ind['gender'].append('men')
			if ind.women > 0:
				ind['gender'].append('women')
			if ind.boys > 0:
				ind['gender'].append('boys')
			if ind.girls > 0:
				ind['gender'].append('girls')
		else:
			ind['gender'].append('total')

		for year in years:
			for month in years[year]:
				ind['months'].setdefault(cstr(month['date']), {})
				ind['months'][cstr(month["date"])]['men'] = 0
				ind['months'][cstr(month["date"])]['women'] = 0
				ind['months'][cstr(month["date"])]['boys'] = 0
				ind['months'][cstr(month["date"])]['girls'] = 0
				ind['months'][cstr(month["date"])]['total'] = 0
				for achiv in log_achiv:
					if achiv['parent'] == ind['log'] and achiv['date'] == month['date'] and achiv['indicator_detail'] == ind['ind_detail']:
						ind['months'][cstr(month["date"])]['men'] = achiv['men']
						ind['months'][cstr(month["date"])]['women'] = achiv['women']
						ind['months'][cstr(month["date"])]['boys'] = achiv['boys']
						ind['months'][cstr(month["date"])]['girls'] = achiv['girls']
						ind['months'][cstr(month["date"])]['total'] = achiv['total']

		result.setdefault(ind['indicator'], [])
		result[ind['indicator']].append(ind)
	return [years, result]

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
	indicator_log = frappe.db.get_value("Indicator Log", {"indicator": indicator['indicator']}, ['name'])
	if not indicator_log:
		return

	log_list = frappe.get_all('Achieved Indicators', filters = {"parent": indicator_log, 'parenttype': 'Indicator Log',
	'indicator_detail': indicator['ind_detail'], }, fields = ['name', 'idx', 'date'])

	# log_ = frappe.get_value('Achieved Indicators', {"parent": indicator_log.name, 'parenttype': 'Indicator Log',
	# 'indicator_detail': indicator['ind_detail'], 'date': indicator['date'],}, ['name', 'idx', 'date'], as_dict = 1)

	date = frappe.utils.getdate(indicator['date'])
	
	last_total = 0
	total = int(indicator['value'])
	value = int(indicator['value'])
	last_name = None
	for log in log_list:
		if log.date == date:
			last_name = log.name
	
	if last_name:
		achieved = frappe.get_doc("Achieved Indicators", last_name)
		last_total = achieved.total
		last_gender = achieved.get(indicator['gender'])
		achieved.update({
			indicator['gender']: value, 
			"idx": (log_list[-1].idx + 1) if log_list else 1,})

		if indicator['gender'] != 'total':
			total = achieved.total - last_gender + value
			achieved.update({'total': total, 'unclassified': 0,})

		else:
			achieved.update({'unclassified': value,})

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
			"hhs": temp.hhs,
			"month": indicator['month'],
			"date": date,
			"indicator_detail": indicator['ind_detail'],
			"parent": indicator_log,
			"parenttype": 'Indicator Log',
			"parentfield": "achieved_indicators",
			"idx": (log_list[-1].idx + 1) if log_list else 1,
		})
		achieved.update({indicator['gender']: value,})
		if indicator['gender'] != 'total':
			achieved.update({'total': value, 'unclassified': 0,})
		else:
			achieved.update({'unclassified': value})

		achieved.insert()

	# last_ind_total = frappe.db.get_value("Indicator Log", {"indicator": indicator['indicator']}, ['total_achieved'])	
	# t = last_ind_total - last_total + total
	# frappe.db.set_value('Indicator Log', {"indicator": indicator['indicator']}, 'total_achieved', t)

	ind_log = frappe.get_doc("Indicator Log", indicator_log)

	log_list = frappe.get_all('Achieved Indicators', filters = {"parent": indicator_log, 'parenttype': 'Indicator Log',
	'indicator_detail': indicator['ind_detail'], }, fields = ['men', 'women', 'boys', 'girls', 'unclassified', 'total'])


	total_m = 0
	total_w = 0
	total_b = 0
	total_g = 0
	total_u = 0
	total_t = 0
	for log in log_list:
		total_m += log.men
		total_w += log.women
		total_b += log.boys
		total_g += log.girls
		total_u += log.unclassified
		total_t += log.total
	
	ind_log.achieved_men = total_m
	ind_log.achieved_women = total_w
	ind_log.achieved_boys = total_b
	ind_log.achieved_girls = total_g
	ind_log.achieved_unclassified = total_u
	ind_log.total_achieved = total_t

	if ind_log.total and ind_log.total_achieved:
		rem = ind_log.total - ind_log.total_achieved
		ind_log.remaining = rem
		final = flt(ind_log.total_achieved / ind_log.total * 100)
		finald = flt(ind_log.remaining / ind_log.total * 100)
		ind_log.cumulative_progress = final
		ind_log.in_progress = finald

	ind_log.save()	
