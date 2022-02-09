// Copyright (c) 2016, Akram Mutaher and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Complaint Mechanism Report"] = {
	"filters": [
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"reqd": 0 ,
			"options": [
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			]
		},

		{
            fieldname: 'complain_mechanism',
            label: __('Complaint Mechanism'),
            fieldtype: 'Link',
			options: 'Complain Mechanism'       
		},
		{
            fieldname: 'project',
            label: __('Project'),
            fieldtype: 'Link',
			options: 'Project'       
		},
	]
};