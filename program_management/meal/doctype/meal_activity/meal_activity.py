# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _, throw
from frappe.utils import add_days, cstr, date_diff, get_link_to_form, getdate
from frappe.utils.nestedset import NestedSet
from frappe.desk.form.assign_to import close_all_assignments, clear
from frappe.utils import date_diff
from frappe.model.document import Document

class CircularReferenceError(frappe.ValidationError): pass
class EndDateCannotBeGreaterThanProjectEndDateError(frappe.ValidationError): pass

class MEALActivity(NestedSet):
	nsm_parent_field = 'parent_meal_activity'

	def populate_depends_on(self):
		if self.parent_meal_activity:
			parent = frappe.get_doc('MEAL Activity', self.parent_meal_activity)
			if not self.name in [row.meal_activity for row in parent.depends_on]:
				parent.append("depends_on", {
					"doctype": "MEAL Activity Depends On",
					"meal_activity": self.name,
					"subject": self.subject
				})
				parent.save()

	def on_trash(self):
		NestedSet.on_trash(self, allow_root_deletion = True)				

@frappe.whitelist()
def check_if_child_exists(name):
	child_tasks = frappe.get_all("MEAL Activity", filters={"parent_meal_activity": name})
	child_tasks = [get_link_to_form("MEAL Activity", meal_activity.name) for meal_activity in child_tasks]
	return child_tasks


 
@frappe.whitelist()
def get_children(doctype, parent, meal_activity=None, project=None, is_root=False):

	filters = [['docstatus', '<', '2']]

	if meal_activity:
		filters.append(['parent_meal_activity', '=', meal_activity])
	elif parent and not is_root:
		# via expand child
		filters.append(['parent_meal_activity', '=', parent])
	else:
		filters.append(['ifnull(`parent_meal_activity`, "")', '=', ''])

	if project:
		filters.append(['project', '=', project])

	activities = frappe.get_list(doctype, fields=[
		'name as value',
		'subject as title',
		'is_group as expandable'
	], filters=filters, order_by='name')

	# return activities
	return activities

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "subject"
	})
	args = make_tree_args(**args)

	if args.parent_meal_activity == 'All MEAL Activity' or args.parent_meal_activity == args.project:
		args.parent_meal_activity = None

	frappe.get_doc(args).insert()

@frappe.whitelist()
def add_multiple_meal_activity(data, parent):
	data = json.loads(data)
	new_doc = {'doctype': 'MEAL Activity', 'parent_meal_activity': parent if parent!="All MEAL Activity" else ""}
	new_doc['project'] = frappe.db.get_value('MEAL Activity', {"name": parent}, 'project') or ""

	for d in data:
		if not d.get("subject"): continue
		new_doc['subject'] = d.get("subject")
		new_meal_activity = frappe.get_doc(new_doc)
		new_meal_activity.insert()