// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Plan', {
	refresh: function(frm) {
		frm.set_df_property("get_activity", "hidden", frm.doc.__islocal ? 1:0);

	},
	get_activity: function(frm){
		frm.events.fill_activity(frm);
	},
	fill_activity: function (frm) {
		var project = frm.doc.project;
		if (!project)
		return;
		
		console.log(project);
		frappe.call({
			method: 'program_management.program_management.doctype.work_plan.work_plan.fill_activity',
			args: {'project': project},
			freeze: true,
			callback: function(r) {
				if (r.message){
					frm.clear_table("work_plan_details");
						r.message.forEach(function(d){
							var new_row = frm.add_child("work_plan_details");
							new_row.activity = d.activity;
							new_row.activity_name = d.activity_name;
					   });
					frm.refresh_field("work_plan_details");
					frm.save();
					frm.refresh();
				}
			}
		})
	}
});

frappe.ui.form.on('Work Plan', {
	setup: function(frm) {
    	frm.fields_dict['work_plan_details'].grid.get_field('output').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
					"project_proposal": frm.project_proposal
				}
			}
	    }	   
	}
})


frappe.ui.form.on('Work Plan', {
	refresh(frm) {
	cur_frm.set_query("activity", "work_plan_details", function(doc, cdt, cdn) {
	    var d = locals[cdt][cdn];
    	return{
	    	filters: [
		    
		    	['Project Activity', 'output', '=', d.output]
	    	]
            	}
        });
	}
})
