// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Implementation Plan Tool', {
	setup: function(frm) {
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			frappe.route_options = null;
		} else {
			// frm.trigger("project");
		}
		frm.disable_save();
		frm.page.clear_activity();

	},
	project: function(frm) {
		frm.events.get_activity(frm);
	},
	get_activity: function(frm){
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api_implementation_plan.get_project_activities",
				args: {
					"project": frm.doc.project,		
				},
				freeze:true,
				callback: function(r) {
					$(frm.fields_dict.implementation_html.wrapper).empty();
					if (r.message) {
						frm.doc.years = r.message[0];
						frm.doc.activity = r.message[1];
						console.log(r.message);
						frm.events.render_table(frm);
						for (let value of r.message) {
							if (!value.docstatus) {
								frm.doc.show_submit = true;
								break;
							}
						}
					}
				}
			});
		}
	},

	render_table: function(frm) {
		frm.events.get_marks(frm);
	},

	get_marks: function(frm) {
		console.log("get_marks");
		var table = $(frappe.render_template('implementation_plan_tool', {
			frm: frm,
			activity: frm.doc.activity,
			years: frm.doc.years,
		}));
		table.appendTo(frm.fields_dict.implementation_html.wrapper);
	
		
	},

});

