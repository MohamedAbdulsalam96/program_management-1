# Copyright (c) 2013, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	data = []

	for pro in get_data(filters):		
		row = [pro.ax_code, pro.name, pro.project_name,get_gov_dis(pro.project_proposal),
			get_sector(pro.project_proposal), get_donor(pro.project_proposal),
			pro.estimated_costing, pro.expected_start_date, pro.final_midterm, pro.expected_end_date, pro.final_final_report,
			pro.status, pro.percent_complete, get_indicator(pro.name)]
		data.append(row)

	# for indicator in data:
	# 	# indicator["total_indicators"] = frappe.db.count("Indicator Log", filters={"project": project.name})
	# 	indicator["over_achieved"] = frappe.db.count("Indicator Log", filters={"project": indicator_log.name, "status": "Over Achieved"})
	# 	indicator["under_achieved"] = frappe.db.count("Indicator Log", filters={"project": indicator.name, "status": "Under Achieved"})	
	# 	indicator["achieved"] = frappe.db.count("Indicator Log", filters={"project": indicator.name, "status": "Achieved"})	

	report_summary = None
	if filters.get("project"):
		if not data:
			report_summary = None
		else:			
			conditions = "  project = '%s'" % filters.get("project")
			conditions2 = "  log.project = '%s'" % filters.get("project")
			total = frappe.db.sql("""SELECT COUNT(name) as total FROM `tabIndicator Log`
				WHERE %s limit 1""" % conditions)
			total_achieved = frappe.db.sql("""SELECT COUNT(name) as total FROM `tabIndicator Log`
				WHERE status='Achieved' and %s limit 1""" % conditions)
			total_under_achieved = frappe.db.sql("""SELECT COUNT(name) as total FROM `tabIndicator Log`
				WHERE status='Under Achieved' and %s limit 1""" % conditions)
			total_over_achieved = frappe.db.sql("""SELECT COUNT(name) as total FROM `tabIndicator Log`
				WHERE status='Over Achieved' and %s limit 1""" % conditions)
			categories = frappe.db.sql("""SELECT det.category as category, SUM(det.total) as total FROM `tabIndicator Log Detail` det
				INNER JOIN `tabIndicator Log` log on det.parent = log.name
				WHERE  %s group by det.category order by SUM(det.total) desc """ % conditions2, as_dict=True)
			pro = frappe.get_doc("Project",filters.get("project"),fields=["percent_complete", "beneficiaries_individual"])
			
			report_summary= [
				{
					"value": total[0][0],
					"indicator": "Blue",
					"label": _("Total Indicators"),
					"datatype": "Int",
				},
				{
					"value": total_achieved[0][0],
					"indicator": "Green",
					"label": _("Total Achieved"),
					"datatype": "Int",
				},
				{
					"value": total_under_achieved[0][0],
					"indicator": "Red",
					"label": _("Total Under Achieved"),
					"datatype": "Int",
				},
				{
					"value": total_over_achieved[0][0],
					"indicator": "Blue",
					"label": _("Total Over Achieved"),
					"datatype": "Int",
				},
				{
					"value": pro.percent_complete,
					"indicator": "Green" if pro.percent_complete > 50 else "Red",
					"label": _("Project Progress"),
					"datatype": "Percent",
				},
				{
					"value": pro.beneficiaries_individual,
					"indicator": "Green",
					"label": _("Beneficiaries Individual"),
					"datatype": "Int",
				}
			]
			if categories:
				for cat in categories:
					report_summary.append({
						"value": cat.total,
						"indicator": "#92A2A2",
						"label": _(cat.category),
						"datatype": "Int",
					})

	return columns, data, None, None, report_summary



def get_conditions(filters):
	conditions = ""
	
	if filters.get("programs"):
		conditions += " LEFT JOIN `tabTargeted Programs` prog on pro.name = prog.parent where prog.program = '%s' " % filters.get("programs")
	elif filters.get("project"):
		conditions += " WHERE pro.name = '%s' " % filters.get("project")

	return conditions

def get_data(filters):
	return frappe.db.sql("""select DISTINCT pro.name, pro.ax_code, pro.name, pro.project_name, pro.project_proposal, pro.status, 
	pro.estimated_costing, pro.percent_complete, pro.expected_start_date, pro.expected_end_date
	from `tabProject` pro  %s""" % get_conditions(filters), as_dict=True)

def get_donor(project_proposal):	
	conditions = "  parent = '%s'" % project_proposal
	donors = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(donor SEPARATOR ', '),"") as donors FROM `tabDonors Details` WHERE %s limit 1""" % conditions)
	return donors[0][0]

def get_sector(project_proposal):	
	conditions = "  parent = '%s'" % project_proposal
	programs = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(program SEPARATOR ', '),"") as programs FROM `tabTargeted Programs`
	WHERE %s limit 1""" % conditions)
	return programs[0][0]

def get_gov_dis(project_proposal):	
	gd=""
	conditions = "  parent = '%s'" % project_proposal
	govs = frappe.db.sql("""SELECT governorate programs FROM `tabGovernorates` WHERE %s """ % conditions, as_list=1)
	for g in govs:
		conditions = "  ter.parent_territory = '%s'" % g[0].replace("'", "\\'")
		conditions += "  and dis.parent = '%s'" % project_proposal
		districts = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(dis.district SEPARATOR ', '),"hh") as districts FROM `tabDistricts` dis
			INNER JOIN `tabTerritory` ter on dis.district = ter.name
			WHERE %s limit 1""" % conditions)
		gd+="[{0}({1})]".format(g[0],districts[0][0])
	return gd

@frappe.whitelist()
def get_indicator(project):	
	conditions = " and project = '%s'" % project
	programs = frappe.db.sql("""SELECT  SUM(total_achieved) indicator FROM `tabIndicator Log` WHERE tracking_beneficiaries = 1
	 %s """ % conditions)
	return programs[0][0]



def get_columns():
	return [
		{
			"fieldname": "ax_code",
			"label": _("AX Code"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "name",
			"label": _("IRY Code"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 170
		},
		{
			"fieldname": "project_name",
			"label": _("Project Title"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "gov_dis",
			"label": _("Targeted Governorate and District"),
			"fieldtype": "Data",
			"width": 400
		},
		{
			"fieldname": "sector",
			"label": _("Sector"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "donor",
			"label": _("Donor"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "estimated_costing",
			"label": _("Total Budget"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "final_start",
			"label": _("Final Start"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "final_midterm",
			"label": _("Final MidTerm"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "final_end",
			"label": _("Final End"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "final_final_report",
			"label": _("Final Final Report"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "percent_complete",
			"label": _("% Completed"),
			"fieldtype": "Percent",
			"width": 120
		},	
		{
			"fieldname": "total",
			"label": _("Beneficiaries Individual"),
			"fieldtype": "float",
			"width": 200
		},
	]

def get_report_summary(data):
	if not data:
		return None

#	# avg_completion = sum(project.percent_complete for project in data) / len(data)
	# total = sum([project.total_tasks for project in data])
	over_achieved = sum([indicators.over_achieved for indicators in data])
#	# completed = sum([project.completed_tasks for project in data])

	return [
		# {
		# 	"value": avg_completion,
		# 	"indicator": "Green" if avg_completion > 50 else "Red",
		# 	"label": _("Average Completion"),
		# 	"datatype": "Percent",
		# },
		# {
		# 	"value": total,
		# 	"indicator": "Blue",
		# 	"label": _("Total Tasks"),
		# 	"datatype": "Int",
		# },
		# {
		# 	"value": completed,
		# 	"indicator": "Green",
		# 	"label": _("Completed Tasks"),
		# 	"datatype": "Int",
		# },
		{
			"value": over_achieved,
			"indicator": "Green" if over_achieved == 0 else "Red",
			"label": _("Overdue Achieved"),
			"datatype": "Int",
		}
	]	