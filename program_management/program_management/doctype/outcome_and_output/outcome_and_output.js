// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outcome and Output', {
	onload: function(frm){
		frm.trigger('source_of_fund');
		frm.trigger('type');
		
	},
	refresh: function(frm) {
		frm.events.filter_(frm);
		frm.set_query("program", function() {
			return {
				query: "program_management.program_management.doctype.targeted_programs.targeted_programs.get_approvers",
				filters: {
					project_proposal: frm.doc.project_proposal,
					doctype: frm.doc.doctype
				}
			};
		});
		
	},
	project: function(frm) {
		frm.events.filter_(frm);
	},
	source_of_fund: function(frm) {
		var op = "";
		if (frm.doc.source_of_fund == "IRW"){
			op = ['Impact', 'Outcome', 'Output'];
			frm.set_df_property('type', 'options', [""].concat(op));
		}	
		else if(frm.doc.source_of_fund == "OCHA"){
			op = ['Objective', 'Outcome', 'Output'];
			frm.set_df_property('type', 'options', [""].concat(op));
		}	
		else if(frm.doc.source_of_fund == "GAC"){
			op = ['Ultimate Outcome', 'Intermediate Outcome', 'Immediate Outcomes', 'Output'];
			frm.set_df_property('type', 'options', [""].concat(op));
		}	

	},

	type: function(frm) {
		if (frm.doc.type == "Impact" || frm.doc.type == "Objective" || frm.doc.type == "Ultimate Outcome" || frm.doc.type == "Project Goal"){
			frm.set_value("is_group", 1);
			frm.set_df_property('program', 'hidden', 1);
			frm.set_df_property('program', 'reqd', 0);
			frm.set_df_property('parent_outcome_and_output', 'hidden', 1);
			frm.set_df_property('parent_outcome_and_output', 'reqd', 0);
		}
		else if (frm.doc.type == "Intermediate Outcome" || frm.doc.type == "Immediate Outcomes" || frm.doc.type == "Outcome"){
			frm.set_value("is_group", 1);
			frm.set_df_property('program', 'hidden', 0);
			frm.set_df_property('program', 'reqd', 1);
			frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
			frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
			
		}

		else if (frm.doc.type == "Output"){
			frm.set_value("is_group", 0);
			frm.set_df_property('program', 'hidden', 0);
			frm.set_df_property('program', 'reqd', 1);
			frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
			frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
			
		}
		// else if (frm.doc.type == "Outcome" || frm.doc.type == "Output"){
		// 	frm.set_value("is_group", 1);
		// 	frm.set_df_property('program', 'hidden', 0);
		// 	frm.set_df_property('program', 'reqd', 1);
		// 	frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
		// 	frm.set_df_property('parent_outcome_and_output', 'reqd', 1);

		// 	frm.events.filter_(frm);
		// }
		else{
			frm.set_value("is_group", 0);
			frm.set_df_property('program', 'hidden', 0);
			frm.set_df_property('program', 'reqd', 1);
			frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
			frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
		}
		frm.events.filter_(frm);
	},
	program: function(frm) {
		frm.events.filter_(frm);
	},

	filter_:function(frm){
			var fil = {
				'project': frm.doc.project,
				'is_group': 1,
			}

			if (frm.doc.source_of_fund != "GAC" && frm.doc.type != "Outcome")
				fil.program = frm.doc.program;
			
			if (frm.doc.source_of_fund == "GAC" && frm.doc.type != "Intermediate Outcome")
				fil.program = frm.doc.program;

			if (frm.doc.type == "Intermediate Outcome")
				fil.type = "Ultimate Outcome";

			else if (frm.doc.type == "Immediate Outcomes")
				fil.type = "Intermediate Outcome";
			
			else if (frm.doc.type == "Output" && frm.doc.source_of_fund	== "GAC")
				fil.type = "Immediate Outcomes";	

			else if (frm.doc.type == "Outcome" && frm.doc.source_of_fund == "IRW")
				fil.type = "Impact";
				
			else if (frm.doc.type == "Output" && frm.doc.source_of_fund == "IRW")
				fil.type = "Outcome";
				
			else if (frm.doc.type == "Outcome" && frm.doc.source_of_fund == "OCHA")
				fil.type = "Objective";	
			
			else if (frm.doc.type == "Output" && frm.doc.source_of_fund == "OCHA")
				fil.type = "Outcome";

			else if (frm.doc.type == "Outcome" && frm.doc.source_of_fund == "SIDA") 
				fil.type = "Project Goal";
			
			else if (frm.doc.type == "Output" && frm.doc.source_of_fund == "SIDA")
				fil.type = "Outcome";	
			// if (frm.doc.type == "Outcome" && frm.doc.source_of_fund	== "IRW")
			//  	fil.type = "Impact";

			// else if (frm.doc.type == "Outcome" && frm.doc.source_of_fund == "OCHA")
			//  	fil.type = "Objective";
			
			// else if (frm.doc.type == "Outcome" && frm.doc.source_of_fund == "SIDA")
			//  	fil.type = "Project Goal";	 	 
			
			// else if (frm.doc.type == "Intermediate Outcome")
			// 	fil.type = "Ultimate Outcome"; 

			// else if (frm.doc.type == "Immediate Outcomes")
			// 	fil.type = "Intermediate Outcome";

			// else if (frm.doc.type == "Output" && frm.doc.source_of_fund == "GAC")
			// 	fil.type = "Immediate Outcomes";	

			// else if (frm.doc.type == "Output" && frm.doc.source_of_fund == "OCHA")
			// 	fil.type = "Outcome";
			
			// else (frm.doc.type == "Output" && frm.doc.source_of_fund == "IRW")
			// 	fil.type = "Outcome";	

			frm.set_query("parent_outcome_and_output", function() {
				return {
					filters: fil
				}
			});
	}
})