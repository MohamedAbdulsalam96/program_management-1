// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('MEAL Checklist Tool', {
	setup: function(frm) {
		// frm.add_fetch("assessment_plan", "student_group", "student_group");
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			// frm.set_value("student_group", frappe.route_options.student_group);
			// frm.set_value("assessment_plan", frappe.route_options.assessment_plan);
			frappe.route_options = null;
		} else {
			frm.trigger("assessment_plan");
		}
		frm.disable_save();
		// frm.page.clear_indicator();
	},

	project: function(frm) {
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api_meal_checklist.get_indicators",
				args: {
					"pro": frm.doc.project					
				},
				callback: function(r) {
					if (r.message) {
						frm.doc.project = r.message;
						frm.events.render_table(frm);
						for (let value of r.message) {
							if (!value.docstatus) {
								frm.doc.show_submit = true;
								break;
							}
						}
						frm.events.submit_result(frm);
					}
				}
			});
		}
	},

	render_table: function(frm) {
		$(frm.fields_dict.checklist_html.wrapper).empty();
			frm.events.get_marks(frm);
	},

	get_marks: function(frm) {

		var meal_plan_table = $(frappe.render_template('meal_checklist_tool', {
			frm: frm,
			project: frm.doc.project
		}));
		meal_plan_table.appendTo(frm.fields_dict.checklist_html.wrapper);

	},

	submit_result: function(frm) {
		if (frm.doc.show_submit) {
			frm.page.set_primary_action(__("Submit"), function() {
				frappe.call({
					method: "program_management.meal.api_meal_plan.submit_assessment_results",
					args: {
						"indicators": frm.doc.indicators						
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__("{0} Result submittted", [r.message]));
						} else {
							frappe.msgprint(__("No Result to submit"));
						}
						frm.events.assessment_plan(frm);
					}
				});
			});
		}
		else {
			frm.page.clear_primary_action();
		}
	}
});
