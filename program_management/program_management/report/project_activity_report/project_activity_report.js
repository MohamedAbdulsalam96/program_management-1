// Copyright (c) 2016, Akram Mutaher and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Activity Report"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["", "Open", "Working","Pending Review","Overdue","Completed"]
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "delay") {
			if (data["delay"] > 0) {
				value = `<p style="color: red; font-weight: bold">${value}</p>`;
			} else {
				value = `<p style="color: green; font-weight: bold">${value}</p>`;
			}
		}
		return value
	}
};
