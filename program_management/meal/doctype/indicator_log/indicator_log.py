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
			self.calc_achieved_indicators()
	
	def calc_achieved_indicators(self):
		self.total_achieved=0
		for ind in self.achieved_indicators:
			if self.is_cumulative:
				self.total_achieved+=ind.total
		if self.total>0:
			if self.is_cumulative:
				self.total_achieved=cint(flt(self.total_achieved)/len(self.achieved_indicators))
				self.cumulative_progress=self.total_achieved/self.total*100
				self.remaining=self.total-self.total_achieved
				self.in_progress=self.remaining/self.total*100