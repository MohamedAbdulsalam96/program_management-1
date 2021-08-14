from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Programs"),
			"items": [
				{
					"type": "doctype",
					"name": "Project Proposal",
					
				},
				{
					"type": "doctype",
					"name": "Programs",
					
				},

				
			]
		},
                {
			"label": _("Logical Framework"),
			"items": [
				{
					"type": "doctype",
					"name": "Outcome and Output",
					"description": _("Outcome and Output.")
					
				},
				{
					"type": "doctype",
					"name": "Indicators",
					"description": _("Indicators.")
					
				},
				{
					"type": "doctype",
					"name": "Activity",
					"description": _("Activity.")
					
				},
				{
					"type": "doctype",
					"name": "Logframes",					
				},
				{
					"type": "report",
					"name": "Logframe Summery Report",	
					"doctype": "Project Proposal",
					"is_query_report": True				
				},
				{
					"type": "doctype",
					"name": "Proposal Documents",
					"description": _("Proposal Documents."),
					"onboard": 1,
				}
			]
		},
                {
			"label": _("Plans"),
			"items": [
				{
					"type": "doctype",
					"name": "Work Plan",
					"description": _("Work Plan."),
					
				},
				{
					"type": "doctype",
					"name": "Risk Plan",
					"description": _("Risk Plan."),
				},
				{
					"type": "doctype",
					"name": "Communication Plan",
					"description": _("Communication Plan.")
				},
				{
					"type": "doctype",
					"name": "Technical Plan for Supervision",
					
				},
				

			]
		},

		{
			"label": _("Communication Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Per Project",
					
				},
				{
					"type": "doctype",
					"name": "Per Coordinate",
				},
				{
					"type": "doctype",
					"name": "Cluster Documents",
				},
			]
		},

		{
			"label": _("Reports"),
			"items": [
				{
					"type": "doctype",
					"name": "Monthly Report",
					"description": _("Monthly Reports for Projects"),
				},
				{
					"type": "doctype",
					"name": "Narrative Report",
				},
				{
					"type": "doctype",
					"name": "Managers Monthly Report",
				},
				]
		},

                {
			"label": _("Volunteer"),
			"items": [
				{
					"type": "doctype",
					"name": "Volunteer",
					"description": _("Volunteer information."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Volunteer Type",
					"description": _("Volunteer Type information."),
				}
			]
		},
		{
			"label": _("Donor"),
			"items": [
				{
					"type": "doctype",
					"name": "Donor",
					"description": _("Donor information."),
				},
				{
					"type": "doctype",
					"name": "Donor Type",
					"description": _("Donor Type information."),
				}
			]
		},

		
	]
