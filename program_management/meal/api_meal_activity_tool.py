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
			select IFNULL(GROUP_CONCAT(ide.governorate SEPARATOR ', '),"") as location
			from `tabIndicator Detail` ide 
			where ide.parent = %s group by ide.parent
		""", (project), as_dict=0)
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	# indicators = frappe.get_list("Indicators", fields=["name","docstatus","indicator","project","linked_with","output","frequency","responsible","meal_activities","location","mean_of_verification","linked_with_outcome","linked_with_objective","total"] ,
	# 	filters={"project": project}, order_by= "output asc")
	return ss_list

# def get_gov(indicators):	
# 	conditions = "parent = '%s'" % project_proposal
# 	govs = frappe.db.sql("""SELECT IFNULL(GROUP_CONCAT(donor SEPARATOR ', '),"") as donors FROM `tabIndicator Detail` WHERE %s limit 1""" % conditions)
# 	return govs[0][0]	

@frappe.whitelist()
def get_project_activity(project):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	filters={"project": project,"is_group":1}	
	outcome_and_outputs = frappe.get_list("MEAL Activity", fields=["main_activity","subject"] ,
		filters=filters, order_by= "main_activity", group_by="main_activity")
	return outcome_and_outputs

@frappe.whitelist()
def get_main_activity(main_activity):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	filters={"type":"MEAL Activity","is_group":1,"main_activity":main_activity}	
	outcome_and_outputs = frappe.get_list("MEAL Activity", fields=["subject","name"] ,
		filters=filters, order_by= "name")
	return outcome_and_outputs

@frappe.whitelist()
def get_sub_activity(parent_meal_activity):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""	
	filters={"type":"MEAL Sub-Activity","is_group":0,"parent_meal_activity":parent_meal_activity}	
	outcome_and_outputs = frappe.get_list("MEAL Activity", fields=["subject","name"] ,
		filters=filters, order_by= "name")

	return outcome_and_outputs


@frappe.whitelist()
def get_indicators(project):
	# ind_list = get_project_indicators(project)
	pro_act_list = get_project_activity(project)
	for i, pro_act in enumerate(pro_act_list):
		main_act_list=get_main_activity(pro_act.main_activity)
		pro_act.update({
			"main_act_list": main_act_list,	
			"main_act_list_len": len(main_act_list),
		})
		for j, main_act in enumerate(main_act_list):
			sub_act_list=get_sub_activity(main_act.name)
			main_act.update({
				"sub_act_list": sub_act_list,
				"sub_act_list_len":len(sub_act_list)
			})	
	# frappe.throw(frappe.as_json(pro_act_list))			
	return pro_act_list


