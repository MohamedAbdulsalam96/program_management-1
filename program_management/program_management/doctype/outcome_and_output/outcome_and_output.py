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

class OutcomeandOutput(NestedSet):
	nsm_parent_field = 'parent_outcome_and_output'

	def populate_depends_on(self):
		if self.parent_outcome_and_output:
			parent = frappe.get_doc('Outcome and Output', self.parent_outcome_and_output)
			if not self.name in [row.outcome_and_output for row in parent.depends_on]:
				parent.append("depends_on", {
					"doctype": "Outcome and Output Depends On",
					"outcome_and_output": self.name,
					"subject": self.subject
				})
				parent.save()

	def on_trash(self):
		NestedSet.on_trash(self, allow_root_deletion = True)				

@frappe.whitelist()
def check_if_child_exists(name):
	child_tasks = frappe.get_all("Outcome and Output", filters={"parent_outcome_and_output": name})
	child_tasks = [get_link_to_form("Outcome and Output", outcome_and_output.name) for outcome_and_output in child_tasks]
	return child_tasks


 
@frappe.whitelist()
def get_children(doctype, parent, outcome_and_output=None, project_proposal=None, is_root=False):

	filters = [['docstatus', '<', '2']]

	if outcome_and_output:
		filters.append(['parent_outcome_and_output', '=', outcome_and_output])
	elif parent and not is_root:
		# via expand child
		filters.append(['parent_outcome_and_output', '=', parent])
	else:
		filters.append(['ifnull(`parent_outcome_and_output`, "")', '=', ''])

	if project_proposal:
		filters.append(['project_proposal', '=', project_proposal])

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

	if args.parent_outcome_and_output == 'All Outcome and Output' or args.parent_outcome_and_output == args.project_proposal:
		args.parent_outcome_and_output = None

	frappe.get_doc(args).insert()

@frappe.whitelist()
def add_multiple_outcome_and_output(data, parent):
	data = json.loads(data)
	new_doc = {'doctype': 'Outcome and Output', 'parent_outcome_and_output': parent if parent!="All Outcome and Output" else ""}
	new_doc['project'] = frappe.db.get_value('Outcome and Output', {"name": parent}, 'project_proposal') or ""

	for d in data:
		if not d.get("subject"): continue
		new_doc['subject'] = d.get("subject")
		new_outcome_and_output = frappe.get_doc(new_doc)
		new_outcome_and_output.insert()

