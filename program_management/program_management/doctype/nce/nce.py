# Copyright (c) 2021, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from program_management.program_management.utils import update_project
from frappe.model.naming import make_autoname
#from program_management.program_management.utils import update_project, validate_completed_project


class NCE(Document):
	def __init__(self, *args, **kwargs):
		super(NCE, self).__init__(*args, **kwargs)
		self.series = 'NCE/{0}/.#####'.format(self.project)

	def autoname(self):
		self.name = make_autoname(self.series)
	# def validate(self):
	# 	validate_completed_project(self.project)

	def before_submit(self):
		pass
		# if getdate(self.extension_date) > getdate():
		# 	frappe.throw(_("Project Extention cannot be submitted before Extention Date"),
		# 		frappe.DocstatusTransitionError)

	def on_submit(self):
		self.update_original_date()
		# project = frappe.get_doc("Project", self.project)
		# project = update_project(project, self.project_extension, date=self.extension_date)
		# project.save()

	def validate(self):
		if self.revised_start_date and self.project_start_date:
			if self.revised_start_date < self.project_start_date:
				frappe.throw(_("Revised Date Should Be Bigger Than Original Start Date"))
		if self.revised_end_date and self.project_end_date:
			if self.revised_end_date < self.revised_start_date:
				frappe.throw(_("Revised End Date Should Be Bigger Than Revised Start Date"))
			if self.revised_end_date < self.project_end_date:
				frappe.throw(_("Revised End Date Should Be Bigger Than Orignal End Date"))
		# chk=self.check_nces()
		# if chk:
		# 	frappe.throw(_("Revised End Date In NCE {0}")).format(chk[0].name)



	def check_nces(self):
		return frappe.db.sql("""select name
		from `tabNCE` 
		where project=%s and  %s between revised_start_date and  revised_end_date
		 """, [self.project,self.revised_end_date], as_dict=True)


	def on_cancel(self):
		project = frappe.get_doc("Project", self.project)
		project.expected_start_date=self.project_start_date
		project.expected_end_date=self.project_end_date
		project.save()
		# project = frappe.get_doc("Project", self.project)
		# project = update_project(project, self.project_extension, cancel=True)
		# project.save()

	def update_original_date(self):
		project = frappe.get_doc("Project", self.project)
		project.expected_start_date=self.revised_start_date
		project.expected_end_date=self.revised_end_date
		from frappe.utils.data import month_diff
		project.project_duration = month_diff(self.revised_end_date, self.revised_start_date)
		project.save()

