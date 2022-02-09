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

class Resources(NestedSet):
	nsm_parent_field = 'parent_resources'

	def populate_depends_on(self):
		if self.parent_resources:
			parent = frappe.get_doc('Resources', self.parent_resources)
			if not self.name in [row.resources for row in parent.depends_on]:
				parent.append("depends_on", {
					"doctype": "Resources Depends On",
					"resources": self.name,
					"resource": self.resource
				})
				parent.save()

	def on_trash(self):
		NestedSet.on_trash(self, allow_root_deletion = True)				

@frappe.whitelist()
def check_if_child_exists(name):
	child_tasks = frappe.get_all("Resources", filters={"parent_resources": name})
	child_tasks = [get_link_to_form("Resources", resources.name) for resources in child_tasks]
	return child_tasks


 
@frappe.whitelist()
def get_children(doctype, parent, resources=None, sector=None, is_root=False):

	filters = [['docstatus', '<', '2']]

	if resources:
		filters.append(['parent_resources', '=', resources])
	elif parent and not is_root:
		# via expand child
		filters.append(['parent_resources', '=', parent])
	else:
		filters.append(['ifnull(`parent_resources`, "")', '=', ''])

	# if project_proposal:
	# 	filters.append(['project_proposal', '=', project_proposal])
	
	if sector:
		filters.append(['sector', '=', sector])	

	activities = frappe.get_list(doctype, fields=[
		'name as value',
		'resource as title',
		'is_group as expandable',
		'attach as attached_file'
	], filters=filters, order_by='name')

	# return activities
	return activities

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "resource"
	})
	args = make_tree_args(**args)

	if args.parent_resources == 'All Resources' or args.parent_resources == args.sector:
		args.parent_resources = None

	frappe.get_doc(args).insert()

@frappe.whitelist()
def add_multiple_resources(data, parent):
	data = json.loads(data)
	new_doc = {'doctype': 'Resources', 'parent_resources': parent if parent!="All Resources" else ""}
	new_doc['sector'] = frappe.db.get_value('Resources', {"name": parent}, 'sector') or ""

	for d in data:
		if not d.get("resource"): continue
		new_doc['resource'] = d.get("resource")
		new_resources = frappe.get_doc(new_doc)
		new_resources.insert()

