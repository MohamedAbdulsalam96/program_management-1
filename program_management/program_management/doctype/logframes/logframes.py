# -*- coding: utf-8 -*-
# Copyright (c) 2021, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Logframes(Document):
	def validate(self):
		self.sort_details_out()
		self.sort_details()
		self.sort_details_acts()
	def get_existing_activity_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql_list("""select indicator as indicator from `tabIndicator Progress Tracking` 
		where parentfield='indicators' and parent=%s order by indicator ASC""",self.name)

	def get_existing_out_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql_list("""select outcome_and_output as outcome_and_output from `tabOutcomes and Outputs` 
		where parentfield='outcome_and_output' and parent=%s order by outcome_and_output ASC""",self.name)

	def get_existing_act_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql_list("""select activity as activity from `tabActivity` 
		where parentfield='activities' and parent=%s order by activity ASC""",self.name)	

	def get_activities_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql("""select acts.name as activity, acts.activity as activity_subject from `tabActivity` acts 
		where acts.project_proposal=%s """,self.project_proposal, as_dict=True)

	def get_out_list(self):
		"""
			Returns list of active employees based on selected criteria
			and for which salary structure exists
		"""
		return frappe.db.sql("""select outs.name as outcome_and_output, outs.subject as subject from `tabOutcome and Output` outs 
		where outs.project_proposal=%s """,self.project_proposal, as_dict=True)

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
		for d in activities:
			if d.indicator not in existing_activities:
				self.append('indicators', d)
		#self.sort_details()

	def fill_out(self):			
		#self.set('work_plan_details', [])
		outs = self.get_out_list()
		if not outs:
			frappe.throw(_("No Logframe for the mentioned project proposal"))
		existing_outs=self.get_existing_out_list()
		for d in outs:
			if d.outcome_and_output not in existing_outs:
				self.append('outcome_and_output', d)

	def fill_activities(self):			
		#self.set('work_plan_details', [])
		outs = self.get_activities_list()
		if not outs:
			frappe.throw(_("No Logframe for the mentioned project proposal"))
		existing_acts=self.get_existing_act_list()
		for d in outs:
			if d.activity not in existing_acts:
				self.append('activities', d)

		#self.sort_details()
	def sort_details(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.indicators, key=lambda item: item.indicator), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem
	def sort_details_out(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.outcome_and_output, key=lambda item: item.outcome_and_output), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem

	def sort_details_acts(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.activities, key=lambda item: item.activity), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem