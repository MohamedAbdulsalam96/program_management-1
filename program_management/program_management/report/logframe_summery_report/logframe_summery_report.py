# Copyright (c) 2021, farouk muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint
from frappe import _
from collections import defaultdict
from erpnext.setup.utils import get_exchange_rate
from frappe.utils import (flt,cstr)

def execute(filters=None):

	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_conditions(filters):
	conditions = []
	if filters.get("name"): conditions.append("name = %(name)s")
	#if filters.get("project"): conditions.append("project = %(project)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""

def get_columns():
	return [
		{
			"fieldname": "subject",
			"label": _("Subject"),
			"fieldtype": "Data",
			"width": 1100
		},
		{
			"fieldname": "planned",
			"label": _("Planned"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "achieved",
			"label": _("Achieved"),
			"fieldtype": "Data",
			"width": 100
		},
	]

def get_proposal(filters):
	return frappe.db.sql("""SELECT name, project_title FROM `tabProject Proposal` 
	{conditions} order by name ASC""".format(conditions=get_conditions(filters),), filters, as_dict=1)

def get_project(proposal):
	return frappe.db.sql("""SELECT name, project_code, project_name FROM `tabProject` WHERE project_proposal=%s order by name ASC""",proposal, as_dict=True)

def get_in_out_obj(prop):
	return frappe.db.sql("""SELECT name, code, subject FROM `tabOutcome and Output`
     WHERE project_proposal=%s and type = 'Objective' order by name ASC""", prop, as_dict=True)

def get_in_out2(filters):
	return frappe.db.sql("""SELECT name, code, subject FROM `tabOutcome and Output`
     WHERE project_proposal=%(prop)s and type = %(type)s and parent_outcome_and_output = %(parent)s order by name ASC""",filters, as_dict=True)


# def get_indicator_log(in_out):
# 	return frappe.db.sql("""SELECT name, indicator, total_achieved FROM `tabIndicators`
#      WHERE output=%s and is_percentage = false order by name ASC""", in_out, as_dict=True)

def get_indicator_log(in_out):
	data = frappe.db.sql("""
		SELECT
			ind.name, ind.code, ind.indicator, ind.is_percentage, log.total, log.total_achieved
		FROM
			`tabIndicators` ind
		INNER JOIN `tabIndicator Log` log
        ON ind.name = log.indicator
        WHERE ind.output=%s
		order by log.name desc""", in_out, as_dict=1)

	return data

def get_work_plan(in_out):
	data = frappe.db.sql("""
		SELECT
			act.name, act.code, act.activity, log.activity_name, log.progress
		FROM
			`tabActivity` act
		INNER JOIN `tabWork Plan Log` log
        ON act.name = log.activity
        WHERE act.output=%s and log.is_group=1
		order by act.code asc""", in_out, as_dict=1)

	return data

def get_data(conditions):
	alltree = {}
	count = 0
	percount = 0
	objcount = 0
	pertotal = 0
	objtotal = 0
	pertotalper = 0
	objtotalper = 0
	totalcount = 0

	totalPlanned = 0
	totalAchieved = 0
	lastCount = 0
	for prop in get_proposal(conditions):
		count += 1
		alltree[count] = {}
		alltree[count].setdefault(count)
		alltree[count]['name']=prop.name
		alltree[count]['subject']= prop.name + ' - ' + prop.project_title if prop.name and prop.project_title else prop.name
		alltree[count]['planned']='.'
		alltree[count]['achieved']='.'
		alltree[count]['parent']=None
		alltree[count]['indent']=0
		pertotal = 0
		percount = count
		for proj in get_project(prop.name):
			count += 1
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']=proj.name
			alltree[count]['subject']= proj.project_code + ' - ' + proj.project_name if proj.project_code and proj.project_name else proj.project_name 
			alltree[count]['planned']=None
			alltree[count]['achieved']=None
			alltree[count]['parent']=prop.name
			alltree[count]['indent']=1
			objtotal = 0
			objcount = count
			for obj in get_in_out_obj(prop.name):
				count += 1
				alltree[count] = {}
				alltree[count].setdefault(count)
				alltree[count]['name']=obj.name
				alltree[count]['subject']= '(objective) ' + obj.code + ' - ' + obj.subject if obj.code and obj.subject else obj.subject
				alltree[count]['planned']=None
				alltree[count]['achieved']=None
				alltree[count]['parent']=proj.name
				alltree[count]['indent'] = 2
				for outcome in get_in_out2( {'prop':prop.name, 'type':'Outcome', 'parent':obj.name}):
					count += 1
					alltree[count] = {}
					alltree[count].setdefault(count)
					alltree[count]['name']=outcome.name
					alltree[count]['subject']= '(outcome) ' + outcome.code + ' - ' + outcome.subject if outcome.code and outcome.subject else outcome.subject
					alltree[count]['planned']=None
					alltree[count]['achieved']=None
					alltree[count]['parent']=obj.name
					alltree[count]['indent'] = 3
					for output in get_in_out2({'prop':prop.name, 'type':'Output', 'parent':outcome.name}):
						count += 1
						alltree[count] = {}
						alltree[count].setdefault(count)
						alltree[count]['name']=output.name
						alltree[count]['subject']= '(output) ' + outcome.code + ' - ' + outcome.subject  if outcome.code and outcome.subject else outcome.subject
						alltree[count]['achieved']=None
						alltree[count]['parent']=outcome.name
						alltree[count]['indent'] = 4
						for in_ac in [1,2]:
							count += 1
							alltree[count] = {}
							alltree[count].setdefault(count)
							alltree[count]['name']= in_ac
							alltree[count]['parent']=output.name
							alltree[count]['indent'] = 5
							if in_ac == 1:
								totalAchieved = 0
								totalPlanned = 0
								alltree[count]['subject']='Indicators'
								lastCount = count
								for ind in get_indicator_log(output.name):
									count += 1
									alltree[count] = {}
									alltree[count].setdefault(count)
									alltree[count]['name']=ind.name
									alltree[count]['subject']= ind.code + ' - ' + ind.indicator if ind.code and ind.indicator else ind.indicator
									alltree[count]['parent']= in_ac
									alltree[count]['indent'] = 6
									if(not ind.is_percentage):
										totalPlanned += ind.total
										totalAchieved += ind.total_achieved
										alltree[count]['planned']=ind.total
										alltree[count]['achieved']=flt(ind.total_achieved,2)
									else:
										alltree[count]['planned']=str(ind.total) + " % "
										alltree[count]['achieved']=str(flt(ind.total_achieved,2)) + " % "
										
								alltree[lastCount]['planned']=totalPlanned
								alltree[lastCount]['achieved']=totalAchieved
							else:
								totalAchieved = 0
								totalPlanned = 0
								workCount = 0
								alltree[count]['subject']= 'Activities'
								lastCount = count
								for plan in get_work_plan(output.name):
									count += 1
									workCount += 1
									alltree[count] = {}
									alltree[count].setdefault(count)
									alltree[count]['name']=plan.name
									alltree[count]['subject']= plan.code + ' - ' + plan.activity if plan.code and plan.activity else plan.activity
									alltree[count]['planned']=str(100) + " % "
									alltree[count]['achieved']=str(flt(plan.progress,2)) + " % "
									alltree[count]['parent']=in_ac
									alltree[count]['indent'] = 6
									totalPlanned += plan.progress

								alltree[lastCount]['planned']=str(100) + " % "
								workPer = 1
								if workCount != 0:
									workPer = 100 / workCount
								alltree[lastCount]['achieved']= str(flt(totalPlanned,2) / 100 * flt(workPer,2)) + " % "
								

			
	
	data = []
	for t in sorted(alltree):

		tree = alltree.get(t)
		row = {
			"name": tree.get('name',''),
			"subject": tree.get('subject',''),
			"planned": tree.get('planned',''),
			"achieved": tree.get('achieved',''),
			"parent": tree.get('parent',''),
			"indent": tree.get('indent',''),
		}
		data.append(row)
	return data


