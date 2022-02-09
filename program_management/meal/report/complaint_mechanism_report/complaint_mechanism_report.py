# Copyright (c) 2013, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()

	data = []
	for comp in get_data(filters):
		mon={
			1:"Jan",
			2:"Feb",
			3:"Mar",
			4:"Apr",
			5:"May",
			6:"June",
			7:"July",
			8:"Aug",
			9:"Sep",
			10:"Oct",
			11:"Nov",
			12:"Dec",
		}
		docstatus={
			0:"Draft",
			1:"Submitted",
			2:"Cancelled",			
		}		
		row = [comp.name, comp.date_of_complain, mon[comp.date_of_complain_month], comp.name_of_complainant, comp.gender, comp.mobile_number, comp.governorate, comp.district,
		comp.program, comp.project, comp.project_name, comp.complaints_category, comp.complaint_type_weight, comp.complaint_description, comp.recipient_name,
		docstatus[comp.docstatus], comp.concerned_with_resolving_name, comp.action_taken, comp.concerned_with_resolving_name, comp.closing_date, comp.complaint_status]
		data.append(row)

		# row = [comp.name, comp.ax_code, comp.project, comp.project_name, comp.date_of_complain, comp.mechanism_used, comp.name_of_complainant, comp.program,
		# comp.gender, comp.mobile_number, comp.age_group, comp.complaints_category, comp.complaint_type_weight, comp.recipient_name,
		# comp.complaint_description, comp.concerned_with_resolving_name, comp.reason_of_complaint, comp.action_taken, comp.complaint_status, comp.closing_date]
		# data.append(row)


	return columns, data

# def get_conditions(filters):
# 	conditions = ""
# 	if filters.get("complain_mechanism"):
# 		conditions += " WHERE name = '%s' " % filters.get("complain_mechanism")

# 	if filters.get("month"): conditions.append(" month(date_of_complain) = %(month)s")
	

# 	return conditions

def get_conditions(filters):
	conditions = []
	if filters.get("complain_mechanism"): conditions.append(" name = %(complain_mechanism)s ")
	if filters.get("month"): conditions.append(" month(date_of_complain) = %(month)s ")	
	return " where {}".format(" and ".join(conditions)) if conditions else ""

def get_data(filters):
	return frappe.db.sql("""select name, date_of_complain, month(date_of_complain) as date_of_complain_month, name_of_complainant, gender, mobile_number, governorate, district,
		program, project, project_name, complaints_category, complaint_type_weight, complaint_description, recipient_name,
		docstatus, concerned_with_resolving_name, action_taken, concerned_with_resolving_name, closing_date, complaint_status
		from `tabComplain Mechanism` {conditions}""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=True)


def get_columns():
	return [
		{
			"fieldname": "complain_mechanism",
			"label": _("Complain Mechanism"),
			"fieldtype": "link",
			"options": "Complain Mechanism",
			"width": 180
		},
		{
			"fieldname": "date_of_complain",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 150
		},
		{
			"fieldname": "date_of_complain_month",
			"label": _("Month"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "name_of_complainant",
			"label": _("Complainant/s Name"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "gender",
			"label": _("Complainant/s Gender"),
			"fieldtype": "Date",
			"width": 150
		},
		{
			"fieldname": "mobile_number",
			"label": _("Complainant/s Contact Mobile No."),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "governorate",
			"label": _("Cite"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "district",
			"label": _("District"),
			"fieldtype": "",
			"width": 150
		},
		{
			"fieldname": "program",
			"label": _("Sector"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "project",
			"label": _("Project's Pin Code"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "project_name",
			"label": _("Project's Name"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "complaints_category",
			"label": _("Complaint Category"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "complaint_type_weight",
			"label": _("Complaint Weight"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "complaint_description",
			"label": _("Description of Feedback or Complaint / Allegation / Issue"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "recipient_name",
			"label": _("Received by"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "docstatus",
			"label": _("Current Status"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "concerned_with_resolving_name",
			"label": _("Who has the Feedback"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "action_taken",
			"label": _("What Action"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "concerned_with_resolving_name,",
			"label": _("Closing By"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "closing_date",
			"label": _("Closing Date"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "complaint_status",
			"label": _("Final Status"),
			"fieldtype": "Data",
			"width": 200
		}
	]