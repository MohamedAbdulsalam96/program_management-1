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
def get_project_indicators(project):
	ss_list = frappe.db.sql("""
			select log.name, log.remaining, log.cumulative_progress, log.in_progress, log.indicator_weight, log.achieved_against_project,
			log.total, log.indicator_subject, log.indicator, log.total_achieved,
			ind.code, ind.responsible
			from `tabIndicator Log` log
			INNER JOIN `tabIndicators` ind on log.indicator = ind.name
			where ind.project = %s 
		""", [project], as_dict=1)
	
	# indicators = frappe.get_list("Indicators", fields=["name","docstatus","indicator","project","linked_with","output","frequency","responsible","meal_activities","location","mean_of_verification","linked_with_outcome","linked_with_objective","total"] ,
	# 	filters={"project": project}, order_by= "output asc")

	for ss in ss_list:
		ss.cumulative_progress = flt(ss.cumulative_progress, 2)
		ss.achieved_against_project = flt(ss.achieved_against_project, 2)
		ss.achieved_against_project = flt(ss.achieved_against_project, 2)
		ss.in_progress = flt(ss.in_progress, 2)
	return ss_list

@frappe.whitelist()
def get_project_outcome_and_output(project,type,objective=None,outcome=None,output=None):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	filters={"project": project,"type":type}
	if type=="Outcome" or type=="Output":
		if type=="Outcome":
			filters.update({
				"type": ['in',("Outcome","Immediate Outcomes","Intermediate Outcome")]
			})
		if objective:					
			filters.update({
				"parent_outcome_and_output": objective
			})
		elif outcome:					
			filters.update({
				"parent_outcome_and_output": outcome
			})
	elif type=="Objective":
		filters.update({
			"type": ['in',("Objective","Impact","Project Goal","Ultimate Outcome")]
		})
	outcome_and_outputs = frappe.get_list("Outcome and Output", fields=["name","docstatus","subject","project","code","type"] ,
		filters=filters, order_by= "name asc")
	return outcome_and_outputs

@frappe.whitelist()
def get_project_outcome_and_output_indicators(project,output):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	filters={"project": project,"output":output}
	inds = frappe.get_list("Indicators", fields=["code","name","docstatus","indicator","project","linked_with","output","frequency","responsible","important_assumptions","location","mean_of_verification","total"] ,
		filters=filters, order_by= "name asc")
	return inds


@frappe.whitelist()
def get_indicators(project):
	obj_list = get_project_outcome_and_output(project,"Objective")
	for i, obj in enumerate(obj_list):
		outcome_list=get_project_outcome_and_output(project,"Outcome",objective=obj.name)
		obj.update({
			"outcomes": outcome_list,
			"outcomes_len": len(outcome_list),
			"has_multi_outcome":False
		})
		indicator_list=get_project_outcome_and_output_indicators(project,obj.name)
		obj.update({
			"indicators": indicator_list,
			"indicators_len":len(indicator_list)
		})
		for j, outcome in enumerate(outcome_list):
			output_list=get_project_outcome_and_output(project,"Output",outcome=outcome.name)
			outcome.update({
				"outputs": output_list,
				"outputs_len":len(output_list)
			})
			indicator_list=get_project_outcome_and_output_indicators(project,outcome.name)
			outcome.update({
				"indicators": indicator_list,
				"indicators_len":len(indicator_list)
			})
			for y, output in enumerate(output_list):
				indicator_list=get_project_outcome_and_output_indicators(project,output.name)
				output.update({
					"indicators": indicator_list,
					"indicators_len":len(indicator_list)
				})
			# 
			outcome_list2=get_project_outcome_and_output(project,"Outcome",objective=outcome.name)
			outcome.update({
				"outcomes": outcome_list2,
				"outcomes_len": len(outcome_list2)
			})
			for z, outcome2 in enumerate(outcome_list2):
				
				output_list=get_project_outcome_and_output(project,"Output",outcome=outcome2.name)
				outcome2.update({
					"outputs": output_list,
					"outputs_len":len(output_list)
				})
				indicator_list=get_project_outcome_and_output_indicators(project,outcome2.name)
				outcome2.update({
					"indicators": indicator_list,
					"indicators_len":len(indicator_list)
				})
				obj.update({
					"has_multi_outcome":True
				})
				# obj["outcomes"].append(outcome2)
				for x, output in enumerate(output_list):
					indicator_list=get_project_outcome_and_output_indicators(project,output.name)
					output.update({
						"indicators": indicator_list,
						"indicators_len":len(indicator_list)
					})
					outcome["outputs"].append(output)
		
	return obj_list