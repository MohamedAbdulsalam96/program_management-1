from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ManagersMonthlyReport(Document):
	def validate(self):
		self.sort_details()

	def get_existing_activity_list(self):
		"""
			Returns list of activity based on selected criteria
			and for which project proposal exists
		"""
		return frappe.db.sql_list("""select activity as activity from `tabReport Details` 
		where parentfield='report_details' and parent=%s order by activity ASC""",self.name)

	def get_activity_list(self):
		"""
			Returns list of activity based on selected criteria
			and for which project proposal exists
		"""
		return frappe.db.sql("""select ac.name as activity, ac.activity as activity_name from `tabActivity` ac 
		where ac.project_proposal=%s """,self.project_proposal, as_dict=True)

	def fill_activity(self):			
		#self.set('work_plan_details', [])
		activities = self.get_activity_list()
		if not activities:
			frappe.throw(_("No activities for the mentioned project proposal"))
		existing_activities=self.get_existing_activity_list()
		for d in activities:
			if d.activity not in existing_activities:
				self.append('report_details', d)
		#self.sort_details()

	def sort_details(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.report_details, key=lambda item: item.activity), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem