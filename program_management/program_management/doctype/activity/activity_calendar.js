// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Activity"] = {
	field_map: {
		"start": "start_date",
		"end": "end_date",
		"id": "name",
		"title": "activity",
		"allDay": "allDay",
		"progress": "progress"
	},
	
	gantt: true,
	
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		}
	],
	get_events_method: "frappe.desk.calendar.get_events"
}