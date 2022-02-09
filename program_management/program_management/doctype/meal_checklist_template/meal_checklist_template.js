// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('MEAL Checklist Template', {
	validate: function(frm) {
		var i=0;
		// frm.doc.items.forEach(function(d){
		frm.doc.analysis_and_design_stage.forEach(function(analysis) {
			 analysis.no =i++;
			}); 
		i=0;
		frm.doc.planning_stage.forEach(function(planing) {
		planing.no =i++;	
			
		}); 
		i=0;
		frm.doc.implementation_stage.forEach(function(impl) {
		impl.no =i++;	
			
		}); 

		i=0;
		frm.doc.evaluations_and_reporting_and_project_closure_stage.forEach(function(eva) {
		eva.no =i++;	
			
		}); 


	}
});
