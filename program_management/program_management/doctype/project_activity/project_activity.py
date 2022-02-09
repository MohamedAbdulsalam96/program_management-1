# Copyright (c) 2021, Akram Mutaher and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cstr, getdate


class ProjectActivity(Document):
	def validate(self):
		self.validate_dates()
		self.validate_progress()
		self.check_status()


	def validate_dates(self):
		proj_date = frappe.db.get_value("Project", self.project, ['expected_start_date', 'expected_end_date'])
		if frappe.utils.getdate(self.start_date) < proj_date[0] or frappe.utils.getdate(self.end_date) > proj_date[1]:
			frappe.throw("Start Date Must Be in Project Period")
			

	def validate_progress(self):
		if flt(self.progress or 0) > 100:
			frappe.throw(_("Progress % for a Activity cannot be more than 100."))

		if flt(self.progress) == 100:
			self.status = 'Completed'

		if self.status == 'Completed':
			self.progress = 100

	def update_status(self):
		if self.status not in ('Cancelled', 'Completed') and self.end_date:
			from datetime import datetime
			if getdate(self.end_date) < datetime.now().date():
				self.db_set('status', 'Overdue', update_modified=False)
	
	def check_status(self):
		if self.status not in ('Cancelled', 'Completed') and self.end_date:
			if self.status == "Pending Review":
				if getdate(self.review_date) > getdate(today()):
					return
			from datetime import datetime
			if getdate(self.end_date) < datetime.now().date():
				self.db_set('status', 'Overdue', update_modified=False)


@frappe.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		project_activity = frappe.get_doc("Project Activity", name)
		project_activity.status = status
		project_activity.save()

def set_activities_as_overdue():
	activities = frappe.get_all("Project Activity", filters={"status": ["not in", ["Cancelled", "Completed"]]}, fields=["name", "status", "review_date"])
	for project_activity in activities:
		if project_activity.status == "Pending Review":
			if getdate(project_activity.review_date) > getdate(today()):
				continue
		frappe.get_doc("Project Activity", project_activity.name).update_status()				