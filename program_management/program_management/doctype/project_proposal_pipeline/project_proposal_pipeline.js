// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Proposal Pipeline', {
    refresh(frm) {
		if (frm.doc.docstatus==1){
				frm.add_custom_button(__("Project Proposal"), function () {
					frappe.model.open_mapped_doc({
						method: "program_management.program_management.doctype.project_proposal_pipeline.project_proposal_pipeline.make_project_proposal",
						frm: frm
					});
				},__('Create'));
				frm.page.set_inner_btn_group_as_primary(__('Create'));
		}		
	},
	
});


frappe.ui.form.on("Project Proposal Pipeline", {
	project_proposal_pipeline: function(frm) {
        if(!frm.doc.project_proposal_pipeline)
        return;
        
        	frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Project Proposal Pipeline",
				name: frm.doc.project_proposal_pipeline
			},
			callback: function(data){
				frm.clear_table('donors');
           //frm.fields_dict.table_name_target.grid.remove_all();
				let don = data.message.donors;
		        //let var_name = data.message.table_name_in_template;
				for (var d in don) {
             //for (var iic in var_name){				    
					frm.add_child("donors");
				  //frm.add_child("target_table_name");
					frm.fields_dict.donors.get_value()[d].donor = don[d].donor;
					frm.fields_dict.donors.get_value()[d].donor_name = don[d].donor_name;
				  //frm.fields_dict.target_table_name.get_value()[iic].column_name_in_target_table = var_name[iic].column_name_in_template_table;
				    frm.refresh();
				}
			}
		});

			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Project Proposal",
					name: frm.doc.project_proposal
				},
				callback: function(data){
					frm.clear_table('targeted_programs');
			//frm.fields_dict.table_name_target.grid.remove_all();
					let prog = data.message.targeted_programs;
					//let var_name = data.message.table_name_in_template;
					for (var p in prog) {
				//for (var iic in var_name){				    
						frm.add_child("targeted_programs");
					//frm.add_child("target_table_name");
						frm.fields_dict.targeted_programs.get_value()[p].program = prog[p].program;
						frm.fields_dict.targeted_programs.get_value()[p].percent = prog[p].percent;
					//frm.fields_dict.target_table_name.get_value()[iic].column_name_in_target_table = var_name[iic].column_name_in_template_table;
						frm.refresh();
					}
				}
			});
    },
});