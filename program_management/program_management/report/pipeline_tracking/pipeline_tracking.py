# Copyright (c) 2013, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()

	data = []
	for pip in get_data(filters):		
		row = [pip.name, pip.source_of_fund, get_donor(pip.name), get_sector(pip.name), pip.fund_amount, pip.donor_currency, pip.exchange_rate, pip.amount_lc,
			  pip.fund_confirmation, pip.status_co, pip.co_comment, pip.hq_comment]
		data.append(row)

	return columns, data
	report_summary = get_report_summary(data)

def get_conditions(filters):
	conditions = ""
	if filters.get("project_proposal_pipeline"):
		conditions += " WHERE name = '%s' " % filters.get("project_proposal_pipeline")

	return conditions

def get_data(filters):
	return frappe.db.sql("""select name, source_of_fund, fund_amount, donor_currency, exchange_rate, amount_lc, fund_confirmation, co_comment, status_co, hq_comment
	from `tabProject Proposal Pipeline` %s""" % get_conditions(filters), as_dict=True)

def get_donor(name):	
	conditions = "  parent = '%s'" % name
	donors = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(donor SEPARATOR ', '),"") as donors FROM `tabDonors Details` WHERE %s limit 1""" % conditions)
	return donors[0][0]

def get_sector(name):	
	conditions = "  parent = '%s'" % name
	programs = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(program SEPARATOR ', '),"") as programs FROM `tabTargeted Programs`
	WHERE %s limit 1""" % conditions)
	return programs[0][0]

def get_columns():
	return [
		{
			"fieldname": "project_proposal_pipeline",
			"label": _("Project Proposal Pipeline"),
			"fieldtype": "link",
			"options": "Project Proposal Pipeline",
			"width": 180
		},
		{
			"fieldname": "source_of_fund",
			"label": _("Income Source"),
			"fieldtype": "link",
			"options": "Source Of Fund",
			"width": 150
		},
		{
			"fieldname": "donor",
			"label": _("Donor"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "sector",
			"label": _("Sector"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "fund_amount",
			"label": _("Fund Amount"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "donor_currency",
			"label": _("Donor Currency"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "exchange_rate",
			"label": _("Exchange Rate"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "amount_lc",
			"label": _("Amount LC"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "fund_confirmation",
			"label": _("Fund Confirmation"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status_co",
			"label": _("Status CO"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "co_comment",
			"label": _("CO Comment"),
			"fieldtype": "Data",
			"width": 350
		},
		{
			"fieldname": "hq_comment",
			"label": _("HQ Comment"),
			"fieldtype": "Data",
			"width": 350
		}
	]