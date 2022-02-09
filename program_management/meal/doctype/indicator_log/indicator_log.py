# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint
from frappe.model.document import Document

class IndicatorLog(Document):	
	def validate(self):
		if self.achieved_indicators:
			self.calc_total_achieved()
			self.calculate_finald()
			self.calc_achieved_indicators()
			self.update_project_total_achieved()
		pro=frappe.get_doc("Project",self.project)
		pro.update_percent_complete()
		pro.save()


	def on_update(self):
		self.update_project_achieved_bnf()


	
	def update_project_total_achieved(self):
		if self.tracking_beneficiaries==1:
			if self.total_achieved!=self.total_achieved_2:
				pr = frappe.get_doc("Project", self.project)
				if not pr.total_achieved:
					pr.total_achieved=0
				pr.total_achieved +=(self.total_achieved-self.total_achieved_2)
				self.total_achieved_2=self.total_achieved
				pr.save()
				pr.reload()


	def update_project_achieved_bnf(self):
		if self.tracking_beneficiaries:
			total = frappe.get_all("Indicator Log", 
				filters = {"project": self.project, "tracking_beneficiaries": 1}, 
				fields = ["sum(total_achieved) as total"])

			if total:
				frappe.db.set_value("Project", self.project, "beneficiaries_individual", total[0]["total"])


	
	def calc_achieved_indicators(self):
		for det in self.indicator_log_detail:
			ach_total = 0
			ach_total_u = 0
			idx = 0

			for ach in self.achieved_indicators:
				if det.governorate == ach.governorate:
					idx +=1
					ach_total_u += ach.unclassified
					ach_total += ach.total
					if self.is_percentage:
						ach_total_u = ach_total_u / idx
						ach_total = ach_total_u

			if self.total and self.total_achieved:
				if self.is_cumulative == 1:
					mo = self.months_no
					if (mo == 0):
						mo = 1
					cumulative_progress = flt(ach_total / (len([idx]))) / (det.total * mo) * 100
					det.in_progress = 100 - cumulative_progress
					det.cumulative_progress = cumulative_progress
				else:
					remaining = det.total - ach_total
					det.in_progress = flt(remaining / det.total * 100)
					det.cumulative_progress = flt(ach_total / det.total * 100)
					

		weight_sum = frappe.db.sql("""select sum(indicator_weight) from `tabIndicator Log` where
					project=%s""", self.project)[0][0]
		per = self.cumulative_progress
		# if self.cumulative_progress >= 100:
		# 	per = 100
		pct_complete = per * frappe.utils.safe_div(self.indicator_weight, weight_sum)
		self.achieved_against_project = flt(flt(pct_complete), 2)


	def calc_total_achieved(self):
		total_m = total_w = total_b = total_m = total_w = total_b = total_g = total_u = total_t = total_x = 0
		for i in self.achieved_indicators:
			total_m += i.men
			total_w += i.women
			total_b += i.boys
			total_g += i.girls
			total_u += i.unclassified


		total_t = total_m + total_w + total_b + total_g + total_u

		if self.is_percentage:
			length = len(self.indicator_log_detail)
			total_m /= length
			total_w /= length
			total_b /= length
			total_g /= length
			total_u /= length
			total_t /= length

		self.achieved_men = total_m
		self.achieved_women = total_w
		self.achieved_boys = total_b
		self.achieved_girls = total_g
		self.achieved_unclassified = total_u
		self.total_achieved = total_t


	def calculate_finald(self):
		if self.total and self.total_achieved:
			if self.is_cumulative:
				total_achieved = flt(self.total_achieved/(len(self.achieved_indicators)))

				if self.months_no == 0:
					self.months_no = 1

				self.cumulative_progress = self.total_achieved / (self.total * self.months_no) * 100
				self.remaining = (self.total * self.months_no) - self.total_achieved
				self.in_progress = 100 - self.cumulative_progress

			else:
				self.remaining = self.total - self.total_achieved
				self.cumulative_progress = flt(self.total_achieved / self.total * 100)
				self.in_progress = flt(self.remaining / self.total * 100)
		else:
			self.remaining = self.total * self.months_no if self.is_cumulative else self.total
			self.cumulative_progress = 0
			self.in_progress = 100


def calc_governate_progress(ind, log):
	for det in ind.indicator_detail:
		ach_total = 0
		ach_total_u = 0
		idx = 0
		for ach in log.achieved_indicators:
			if det.governorate == ach.governorate:
				idx +=1
				ach_total_u += ach.unclassified
				ach_total += ach.total
				if log.is_percentage:
					ach_total_u = ach_total_u / log.achieved_indicators.length
					ach_total = ach_total_u

		if log.total and log.total_achieved:
			if log.is_cumulative == 1:
				mo = log.months_no
				if (mo == 0):
					mo = 1
				
				cumulative_progress = flt(ach_total / (len([idx]))) / (det.total * mo) * 100
				det.in_progress = 100 - cumulative_progress
				det.cumulative_progress = cumulative_progress
			else:
				remaining = det.total - ach_total
				det.in_progress = flt(remaining / det.total * 100)
				det.cumulative_progress = flt(ach_total / det.total * 100)