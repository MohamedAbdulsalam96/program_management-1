# Copyright (c) 2013, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import date_diff, nowdate

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	charts = get_chart_data(data)
	return columns, data, None, charts

def get_data(filters):
	conditions = get_conditions(filters)
	activities = frappe.get_all("Project Activity",
			filters = conditions,
			fields = ["project","name", "activity", "project", "start_date", "end_date",
					"status", "linked_with", "output", "progress"],
			order_by="creation"
		)
	for project_activity in activities:
		if project_activity.end_date:
			if project_activity.completed_on:
				project_activity.delay = date_diff(project_activity.completed_on, project_activity.end_date)
			elif project_activity.status == "Completed":
				# task is completed but completed on is not set (for older tasks)
				project_activity.delay = 0
			else:
				# task not completed
				project_activity.delay = date_diff(nowdate(), project_activity.end_date)
		else:
			# task has no end date, hence no delay
			project_activity.delay = 0

	# Sort by descending order of delay
	activities.sort(key=lambda x: x["delay"], reverse=True)
	return activities

def get_conditions(filters):
	conditions = frappe._dict()
	keys = ["status"]
	for key in keys:
		if filters.get(key):
			conditions[key] = filters.get(key)
	if filters.get("from_date"):
		conditions.end_date = [">=", filters.get("from_date")]
	if filters.get("to_date"):
		conditions.start_date = ["<=", filters.get("to_date")]
	if filters.get("project"):
		conditions.project = filters.get("project")
	return conditions

def get_chart_data(data):
	delay, on_track = 0, 0
	for entry in data:
		if entry.get("delay") > 0:
			delay = delay + 1
		else:
			on_track = on_track + 1
	charts = {
		"data": {
			"labels": ["On Track", "Delayed"],
			"datasets": [
				{
					"name": "Delayed",
					"values": [on_track, delay]
				}
			]
		},
		"type": "percentage",
		"colors": ["#84D5BA", "#CB4B5F"]
	}
	return charts

def get_columns():
	columns = [
		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": "Code",
			"options": "Project Activity",
			"width": 150
		},
		{
			"fieldname": "activity",
			"fieldtype": "Data",
			"label": "Activity",
			"width": 200
		},
		{
			"fieldname": "project",
			"fieldtype": "Link",
			"label": "Project",
			"options": "Project",
			"width": 200
		},
		{
			"fieldname": "linked_with",
			"fieldtype": "data",
			"label": "Linked With",
			"width": 200
		},
		{
			"fieldname": "output",
			"fieldtype": "Link",
			"label": "Outcome and Output",
			"options": "Outcome and Output",
			"width": 200
		},
		{
			"fieldname": "status",
			"fieldtype": "Data",
			"label": "Status",
			"width": 100
		},
		{
			"fieldname": "progress",
			"fieldtype": "Percent",
			"label": "Progress (%)",
			"width": 120
		},
		{
			"fieldname": "start_date",
			"fieldtype": "Date",
			"label": "Start Date",
			"width": 150
		},
		{
			"fieldname": "end_date",
			"fieldtype": "Date",
			"label": "End Date",
			"width": 150
		},
		{
			"fieldname": "completed_on",
			"fieldtype": "Date",
			"label": "Actual End Date",
			"width": 130
		},
		{
			"fieldname": "delay",
			"fieldtype": "Data",
			"label": "Delay (In Days)",
			"width": 120
		}
	]
	return columns
