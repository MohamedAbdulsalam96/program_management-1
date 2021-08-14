# Copyright (c) 2013, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		return [], []
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions += " AND project = %(project)s"
	return conditions

def get_data(filters):
	dic = frappe.db.sql("""SELECT name, date, 
	water_q1, water_q3, water_q4, food_q1, food_q2, food_q3, food_q4, test_q, food_q5, shelter_q1, shelter_q2, shelter_q3, 
	shelter_q4, shelterq5, livelihoods_q1, livelihoods_q2, livelihoods_q3, health_q1, health_q2, health_q3, health_q4,
	health_q5, health_q6
	FROM `tabField Survey` 
	""".format(get_conditions(filters)), filters, as_dict=True)

	frappe.msgprint(frappe.as_json(dic))
	
	return dic


def get_columns(filters):
	columns = [_("Disciplinary") + ":Data:180"]
	return columns
