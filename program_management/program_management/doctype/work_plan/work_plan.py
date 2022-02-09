# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class WorkPlan(Document):
	def validate(self):
		self.sort_details()
	def on_submit(self):
		self.create_logs()

	def sort_details(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.work_plan_details, key=lambda item: item.activity), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem

	def create_logs(self):
		doc = frappe.msgprint('Work Plan', self)
		for m in doc.work_plan_details:
			log_args = frappe._dict({
				"doctype": "Work Plan Log",
				"work_plan": doc.name,
				"project": doc.project,
				"activity": m.activity,
				"subject":m.activity,
				"activity_name": m.activity_name,
				"expected_start_date": m.start_date,
				"expected_end_date": m.end_date,
				"is_group":1,
				"planned_duration": m.planned_duration,
			})
			il = frappe.get_doc(log_args)
			il.insert()	

@frappe.whitelist()
def fill_activity(project):			
	#self.set('work_plan_details', [])
	
	activities = frappe.db.sql("""select ac.name as activity, ac.activity as activity_name from `tabProject Activity` ac 
	where ac.project=%s """, project, as_dict=True)	

	if not activities:
		frappe.throw(_("No activities for the mentioned project proposal"))

	work_plan_details = []
	for d in activities:
		work_plan_details.append(d)
	#self.sort_details()
	return work_plan_details

def get_activity_list(project):
	return frappe.db.sql("""select ac.name as activity, ac.activity as activity_name from `tabProject Activity` ac 
	where ac.project=%s """, project, as_dict=True)	


def get_existing_activity_list(work_plan):
	return frappe.db.sql_list("""select activity as activity from `tabWork Plan Details` 
	where parentfield='work_plan_details' and parent=%s order by activity ASC""", work_plan)