// Copyright (c) 2016, Akram Mutaher and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Projects Tracking"] = {
	"filters": [
		{
            fieldname: 'programs',
            label: __('Sector'),
            fieldtype: 'Link',
			options: 'Programs'     
		},
		{
            fieldname: 'project',
            label: __('Project'),
            fieldtype: 'Link',
			options: 'Project'
		},
	]
};
