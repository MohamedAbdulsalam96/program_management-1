# -*- coding: utf-8 -*-
# Copyright (c) 2021, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class NarrativeReport(Document):
	
	def validate(self):
		total_target=0
		total_achieved=0
		for d in self.indicator_progress_tracking:			
			if d.is_percentage==0:
				total_target += d.target
				total_achieved += d.achieved_of_this_month			
		self.total_target=total_target
		self.total_achieved=total_achieved

		self.sort_details()

	def get_existing_activity_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql_list("""select indicator as indicator from `tabIndicator Progress Tracking` 
		where parentfield='indicator_progress_tracking' and parent=%s order by indicator ASC""",self.name)

	def get_indicator_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql("""select ind.name as indicator, ind.indicator_subject as indicator_subject from `tabIndicator Log` ind 
		where ind.project_proposal=%s """,self.project_proposal, as_dict=True)

	def fill_indicators(self):			
		#self.set('work_plan_details', [])
		activities = self.get_indicator_list()
		if not activities:
			frappe.throw(_("No indicators for the mentioned project proposal"))
		existing_activities=self.get_existing_activity_list()
		total_target=0.0
		total_achieved=0.0
		for d in activities:
			if d.indicator not in existing_activities:
				if d.is_percentage==0:
					total_target += d.target
					total_achieved += d.achieved_of_this_month
				self.append('indicator_progress_tracking', d)
		self.total_target=total_target
		self.total_achieved=total_achieved
		#self.sort_details()

	def sort_details(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.indicator_progress_tracking, key=lambda item: item.indicator), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem
