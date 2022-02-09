# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.utils import add_days, flt, cstr, date_diff, get_link_to_form, getdate
from frappe.utils.nestedset import NestedSet, get_root_of
from frappe.desk.form.assign_to import close_all_assignments, clear
from frappe.utils import date_diff
from frappe.model.document import Document

class CircularReferenceError(frappe.ValidationError): pass
class EndDateCannotBeGreaterThanProjectEndDateError(frappe.ValidationError): pass

class WorkPlanLog(NestedSet):
	nsm_parent_field = 'parent_work_plan_log'

	def populate_depends_on(self):
		if self.parent_work_plan_log:
			parent = frappe.get_doc('Work Plan Log', self.parent_work_plan_log)
			if not self.name in [row.work_plan_log for row in parent.depends_on]:
				parent.append("depends_on", {
					"doctype": "Work Plan Log Depends On",
					"work_plan_log": self.name,
					"subject": self.subject
				})
				parent.save()

	def validate(self):
		self.validate_progress()
		self.update_plan()
	def on_trash(self):
		NestedSet.on_trash(self, allow_root_deletion=True)

	def update_plan(self):
		work_plan = frappe.get_doc("Work Plan", self.work_plan)
		for s in work_plan.get("work_plan_details"):
			if s.activity == self.activity:
				s.db_set("status", self.status)
				s.db_set("progress", self.progress)
				s.db_set("actual_start_date", self.actual_start_date)
				s.db_set("actual_end_date", self.actual_end_date)
		work_plan.save()
		work_plan.reload()
	def validate_progress(self):
		if flt(self.progress) >= 100:
			self.status = 'Completed'
		if flt(self.progress) < 100 and flt(self.progress) >0:
			self.status = 'Working'
		if self.parent_work_plan_log:
			parent= frappe.get_doc("Work Plan Log", self.parent_work_plan_log)
			co =frappe.db.sql("SELECT COUNT(DISTINCT (name)) FROM `tabWork Plan Log` where parent_work_plan_log=%s", (self.parent_work_plan_log))
			prog =frappe.db.sql("SELECT sum(progress) FROM `tabWork Plan Log` where parent_work_plan_log=%s and name !=%s", (self.parent_work_plan_log ,self.name))
			if  co[0][0]==0:
				count=1
			else:
				count=co[0][0]
			newprog = (flt(prog[0][0])+flt(self.progress))/count
			parent.db_set("progress",newprog)
			parent.save()
			parent.reload()
		

@frappe.whitelist()
def check_if_child_exists(name):
	child_tasks = frappe.get_all("Work Plan Log", filters={"parent_work_plan_log": name})
	child_tasks = [get_link_to_form("Work Plan Log", work_plan_log.name) for work_plan_log in child_tasks]
	return child_tasks


 
@frappe.whitelist()
def get_children(doctype, parent,project=None, work_plan_log=None, work_plan=None, is_root=False):
	# frappe.msgprint(project)
	if project:
		condition = "a.project=%(project)s"
		var_dict = {
			# "name": get_root_of("Project Activity"),
			"parent": parent,
			"project": project
		}
		# frappe.msgprint("befor")
		if parent:
			if parent==project:
				doctype="Project Activity"
				activities = frappe.db.sql("""
					select
						a.name as value,
						1 as expandable,
						(select IFNULL(sum(l.progress)/count(l.name),0) from `tabWork Plan Log` l where l.activity=a.name group by l.activity) as progress
					from `tab{doctype}` a
					where
						{condition}
					order by name""".format(doctype=doctype, condition=condition), var_dict, as_dict=1)

				# return activities
				# frappe.msgprint(frappe.as_json(activities))
				return activities

			# frappe.msgprint("innnn")
			# frappe.msgprint(parent)
			condition = "activity=%(parent)s"
			return frappe.db.sql("""
				select
					name as value,
					subject as title,
					progress as progress
				from `tabWork Plan Log`
				where is_group=0 and 
					{condition}
				order by name""".format(condition=condition), var_dict, as_dict=1)

		else:
			# frappe.msgprint("not innn")
			condition = "name=%(name)s"
		# frappe.msgprint("after")
		

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "subject"
	})
	args = make_tree_args(**args)

	if args.parent_work_plan_log == 'All Work Plan Log' or args.parent_work_plan_log == args.work_plan:
		args.parent_work_plan_log = None

	frappe.get_doc(args).insert()