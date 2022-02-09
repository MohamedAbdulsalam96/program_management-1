// Copyright (c) 2021, farouk muharram and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Logframe Summery Report"] = {
	"filters": [
		{
			"fieldname": "name",
			"label": __("Sector"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": "80",
		},
		{
			"fieldname": "group_by_sector",
			"label": __("Group By Sector"),
			"fieldtype": "Check",
			"default": 1,
			"width": "80",
		},
		// {
		// 	"fieldname": "project",
		// 	"label": __("Project"),
		// 	"fieldtype": "Link",
		// 	"options": "Project",
		// 	"width": "80",
		// },
	],
	"treeView": true,
	"name_field": "bsc",
	"parent_field": "parent",
	"initial_depth": 0,
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);
		if(column.fieldname == "subject"){
			if(data.indent >= 0 && data.indent <= 5){
				value = `<div style="font-weight:bold">${value}</div>`;
			}

			if(data.indent >= 2 && data.indent <= 4){
				value = `<div style="font-weight:bold">${value}</div>`;
			}
		}
		 if(column.fieldname == "achieved"){
			if(data.achieved == data.planned){
				value = `<div style="color:green">${value}</div>`;
			}else if(data.achieved > data.planned){
				value = `<div style="color:blue">${value}</div>`;
			}else {
				value = `<div style="color:red">${value}</div>`;
			}
		}
		return value;
	},	
};