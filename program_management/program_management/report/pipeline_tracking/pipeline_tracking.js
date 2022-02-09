// Copyright (c) 2016, Akram Mutaher and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pipeline Tracking"] = {
	"filters": [
		{
            fieldname: 'project_proposal_pipeline',
            label: __('Project Proposal Pipeline'),
            fieldtype: 'Link',
			options: 'Project Proposal Pipeline'       
		},
		{
            fieldname: 'source_of_fund',
            label: __('Income Source'),
            fieldtype: 'Link',
			options: 'Source Of Fund'       
		},
		{
            fieldname: 'donor',
            label: __('Donor'),
            fieldtype: 'Link',
			options: 'Customer'       
		},
		{
            fieldname: 'programs',
            label: __('Sector'),
            fieldtype: 'Link',
			options: 'Programs'       
		},

	]
};

