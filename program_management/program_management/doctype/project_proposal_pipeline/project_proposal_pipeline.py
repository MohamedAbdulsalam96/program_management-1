# Copyright (c) 2021, Akram Mutaher and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class ProjectProposalPipeline(Document):
	pass



@frappe.whitelist()
def make_project_proposal(source_name, target_doc=None):
	target_doc = get_mapped_doc("Project Proposal Pipeline", source_name, {
		"Project Proposal Pipeline": {
			"doctype": "Project Proposal",
			"field_map": {
				"name": "project_proposal_pipeline",
				"source_of_fund":"source_of_fund",
				"donor_currency":"project_budget_currency",
				"fund_amount":"project_budget_gbp",
				"amount_lc":"project_budget_usd",
			}

		}
	}, target_doc)
	target_doc.from_assessment = "Project Proposal Pipeline"
	return target_doc