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
	if filters.get("name"): conditions.append("s.program = %(name)s")
	if filters.get("project"): conditions.append("p.name = %(project)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""

def get_columns():
	return [
		{
			"fieldname": "subject",
			"label": _("Subject"),
			"fieldtype": "Data",
			"width": 990
		},
		{
			"fieldname": "planned",
			"label": _("Planned"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "achieved",
			"label": _("Achieved"),
			"fieldtype": "Data",
			"width": 100
		},
	]

def get_proposal_sector(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT pp.name,  pp.project_title 
			FROM `tabProject` p
			INNER JOIN `tabProject Proposal` pp on p.project_proposal = pp.name
			INNER JOIN `tabTargeted Programs` s on pp.name = s.parent
			{conditions}
			group by pp.name order by pp.name ASC""".format(conditions = conditions), filters, as_dict=1)

def get_project(pp):
	return frappe.db.sql("""SELECT p.name, p.project_code, p.project_name, p.project_proposal FROM `tabProject` p
			INNER JOIN `tabProject Proposal` pp on p.project_proposal=pp.name
			WHERE pp.name=%s 
			order by p.name ASC""",pp, as_dict=True)
	

def get_in_out_obj(proj, program):
	return frappe.db.sql("""SELECT name, code, subject, type FROM `tabOutcome and Output`
     WHERE project=%s and (type = 'Objective' or type = 'Impact' or type = 'Ultimate Outcome')
	 order by name ASC""", [proj], as_dict=True)

def get_in_out2(filters):
	return frappe.db.sql("""SELECT name, code, type, subject FROM `tabOutcome and Output`
     WHERE project=%(proj)s and type in %(type)s and parent_outcome_and_output = %(parent)s and program = %(program)s 
	order by name ASC""",filters, as_dict=True)


# def get_indicator_log(in_out):
# 	return frappe.db.sql("""SELECT name, indicator, total_achieved FROM `tabIndicators`
#      WHERE output=%s and is_percentage = false order by name ASC""", in_out, as_dict=True)

def get_indicator_log(in_out, program):
	data = frappe.db.sql("""
		SELECT
			ind.name, ind.code, ind.indicator, ind.is_percentage, log.total, log.total_achieved, ind.tracking_beneficiaries
		FROM
			`tabIndicators` ind
		INNER JOIN `tabIndicator Log` log
        ON ind.name = log.indicator
        WHERE ind.output=%s and program = %s 
		order by log.name desc""", [in_out, program], as_dict=1)

	return data

def get_project_activity(in_out):
	data = frappe.db.sql("""
		SELECT
			act.name, act.code, act.activity, log.activity_name, log.progress
		FROM
			`tabProject Activity` 
        WHERE act.output=%s
		order by act.code asc""", in_out, as_dict=1)

	return data

def get_data(filters):	
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
	for prop in get_proposal_sector(filters):
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
			lastCount5=count
			totalAchieved5 = 0
			totalPlanned5 = 0
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
			for obj in get_in_out_obj(proj.name, filters.get('name')):
				lastCount4=count
				totalAchieved4 = 0
				totalPlanned4 = 0
				count += 1
				alltree[count] = {}
				alltree[count].setdefault(count)
				alltree[count]['name']=obj.name
				alltree[count]['subject']= '('+obj.type+') ' + obj.code + ' - ' + obj.subject if obj.code and obj.subject else obj.subject
				alltree[count]['planned']=None
				alltree[count]['achieved']=None
				alltree[count]['parent']=proj.name
				alltree[count]['indent'] = 2
				for outcome in get_in_out2( {'proj':proj.name, 'type':{'Outcome', 'Intermediate Outcome'}, 'parent':obj.name, 'program':filters.get('name')}):
					lastCount3=count
					totalAchieved3 = 0
					totalPlanned3 = 0
					count += 1
					alltree[count] = {}
					alltree[count].setdefault(count)
					alltree[count]['name']=outcome.name
					alltree[count]['subject']= '(outcome) ' + outcome.code + ' - ' + outcome.name if outcome.code and outcome.subject else outcome.subject
					alltree[count]['planned']=None
					alltree[count]['achieved']=None
					alltree[count]['parent']=obj.name
					alltree[count]['indent'] = 3

					if outcome['type'] == 'Intermediate Outcome':
						count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3 \
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5 = get_resutl_1(proj, 
						outcome, count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3,
						 totalAchieved3, lastCount3,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5
						 , filters)
					else:
						count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3 \
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5 = get_resutl(proj, 
						outcome, count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3,
						 totalAchieved3, lastCount3,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5
						 , filters)
	
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


def get_resutl(proj, outcome, count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5, filters):

	for output in get_in_out2({'proj':proj.name, 'type':{'Output'}, 'parent':outcome.name, 'program':filters.get('name')}):
		
		lastCount2=count
		totalAchieved2 = 0
		totalPlanned2 = 0
		count += 1
		alltree[count] = {}
		alltree[count].setdefault(count)
		alltree[count]['name']=output.name
		alltree[count]['subject']= '(output) ' + output.code + ' - ' + output.name  if output.code and output.subject else output.subject
		alltree[count]['achieved']=None
		alltree[count]['parent']=outcome.name
		alltree[count]['indent'] = 4

		

		lastCount = count
		totalAchieved = 0
		totalPlanned = 0
		count += 1
		in_ac= 'Indicators'
		alltree[count] = {}
		alltree[count].setdefault(count)
		alltree[count]['name']= in_ac
		alltree[count]['subject']= in_ac
		alltree[count]['achieved']= None
		alltree[count]['parent']=output.name
		alltree[count]['indent'] = 5

		
		for ind in get_indicator_log(output.name, filters.get('name')):
			count += 1
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']=ind.name
			alltree[count]['subject']= ind.code + ' - ' + ind.indicator if ind.code and ind.indicator else ind.indicator
			alltree[count]['parent']= in_ac
			alltree[count]['indent'] = 6
			if(not ind.is_percentage):
				

				if ind.tracking_beneficiaries == 1:
					totalPlanned += ind.total
					totalAchieved += ind.total_achieved

					totalPlanned2 += ind.total
					totalAchieved2 += ind.total_achieved

					totalPlanned3 += ind.total
					totalAchieved3 += ind.total_achieved

					totalPlanned4 += ind.total
					totalAchieved4 += ind.total_achieved

					totalPlanned5 += ind.total
					totalAchieved5 += ind.total_achieved

					
				alltree[count]['planned']=ind.total
				alltree[count]['achieved']= ind.total_achieved

			elif ind.is_percentage:
				alltree[count]['planned']=str(ind.total) + " % "
				alltree[count]['achieved']=str(ind.total_achieved) + " % "
		
		count += 1
		alltree[count] = {}
		alltree[count].setdefault(count)
		alltree[count]['name']=None
		alltree[count]['subject']=None
		alltree[count]['parent']=in_ac
		alltree[count]['indent'] = 6
		alltree[count]['planned'] = None
		alltree[count]['achieved'] = None

		alltree[lastCount]['planned']=str(totalPlanned)
		alltree[lastCount]['achieved']=str(totalAchieved)
		alltree[lastCount2]['planned']=None
		alltree[lastCount2]['achieved']=None
		alltree[lastCount3]['planned']= None
		alltree[lastCount3]['achieved']= None
		alltree[lastCount4]['planned']=str(totalPlanned4)
		alltree[lastCount4]['achieved']=str(totalAchieved4)
		alltree[lastCount5]['planned']= None
		alltree[lastCount5]['achieved']= None

	return count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3 \
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5



			# else:
			# 	totalAchieved = 0
			# 	totalPlanned = 0
			# 	workCount = 0
			# 	alltree[count]['subject']= 'Activities'
			# 	lastCount = count
			# 	for plan in get_work_plan(output.name):
			# 		count += 1
			# 		workCount += 1
			# 		alltree[count] = {}
			# 		alltree[count].setdefault(count)
			# 		alltree[count]['name']=plan.name
			# 		alltree[count]['subject']= plan.code + ' - ' + plan.activity if plan.code and plan.activity else plan.activity
			# 		alltree[count]['planned']=str(100) + " % "
			# 		alltree[count]['achieved']=str(flt(plan.progress,2)) + " % "
			# 		alltree[count]['parent']=in_ac
			# 		alltree[count]['indent'] = 6
			# 		totalPlanned += plan.progress

			# 	alltree[lastCount]['planned']=str(100) + " % "
			# 	workPer = 1
			# 	if workCount != 0:
			# 		workPer = 100 / workCount
			# 	alltree[lastCount]['achieved']= str(flt(totalPlanned,2) / 100 * flt(workPer,2)) + " % "

def get_resutl_1(proj, outcome, count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5, filters):
						
	for output1 in get_in_out2({'proj':proj.name, 'type':{'Immediate Outcomes'}, 'parent':outcome.name, 'program':filters.get('name')}):
		lastCount2=count
		totalAchieved2 = 0
		totalPlanned2 = 0
		count += 1
		alltree[count] = {}
		alltree[count].setdefault(count)
		alltree[count]['name']=output1.name
		alltree[count]['subject']= '(output) ' + output1.code + ' - ' + output1.subject  if output1.code and output1.subject else output1.subject
		alltree[count]['achieved']=None
		alltree[count]['parent']=outcome.name
		alltree[count]['indent'] = 4
		
		for output in get_in_out2({'proj':proj.name, 'type':{'Output'}, 'parent':output1.name, 'program':filters.get('name')}):
			lastCount22=count
			totalAchieved22 = 0
			totalPlanned22 = 0
			count += 1
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']=output.name
			alltree[count]['subject']= '(output) ' + output.code + ' - ' + output.subject  if output.code and output.subject else output.subject
			alltree[count]['achieved']=None
			alltree[count]['parent']=output1.name
			alltree[count]['indent'] = 5
			
			lastCount = count
			totalAchieved = 0
			totalPlanned = 0
			count += 1
			in_ac= 'Indicators'
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']= in_ac
			alltree[count]['subject']= in_ac
			alltree[count]['achieved']= None
			alltree[count]['parent']=output.name
			alltree[count]['indent'] = 6
			
			for ind in get_indicator_log(output.name, filters.get('name')):
				count += 1
				alltree[count] = {}
				alltree[count].setdefault(count)
				alltree[count]['name']=ind.name
				alltree[count]['subject']= ind.code + ' - ' + ind.indicator if ind.code and ind.indicator else ind.indicator
				alltree[count]['parent']= in_ac
				alltree[count]['indent'] = 7
				if(not ind.is_percentage ):

					if ind.tracking_beneficiaries == 1:
						totalPlanned += ind.total
						totalAchieved += ind.total_achieved
						totalPlanned2 += ind.total
						totalAchieved2 += ind.total_achieved

						totalPlanned22 += ind.total
						totalAchieved22 += ind.total_achieved

						totalPlanned3 += ind.total
						totalAchieved3 += ind.total_achieved

						totalPlanned4 += ind.total
						totalAchieved4 += ind.total_achieved

						totalPlanned5 += ind.total
						totalAchieved5 += ind.total_achieved

						
					alltree[count]['planned']=ind.total
					alltree[count]['achieved']= ind.total_achieved

				elif ind.is_percentage:
					alltree[count]['planned']=str(ind.total) + " % "
					alltree[count]['achieved']=str(ind.total_achieved) + " % "
			
			count += 1
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']=None
			alltree[count]['subject']=None
			alltree[count]['parent']=in_ac
			alltree[count]['indent'] = 8
			alltree[count]['planned'] = None
			alltree[count]['achieved'] = None

			alltree[lastCount]['planned']=str(totalPlanned)
			alltree[lastCount]['achieved']=str(totalAchieved)
			alltree[lastCount2]['planned']=None
			alltree[lastCount2]['achieved']=None
			alltree[lastCount22]['planned']=None
			alltree[lastCount22]['achieved']=None
			alltree[lastCount3]['planned']= None
			alltree[lastCount3]['achieved']= None
			alltree[lastCount4]['planned']=str(totalPlanned4)
			alltree[lastCount4]['achieved']=str(totalAchieved4)
			alltree[lastCount5]['planned']= None
			alltree[lastCount5]['achieved']= None

	return count, totalAchieved, totalPlanned, lastCount, alltree, totalPlanned3, totalAchieved3, lastCount3 \
						,totalPlanned4, totalAchieved4, lastCount4, totalPlanned5, totalAchieved5, lastCount5