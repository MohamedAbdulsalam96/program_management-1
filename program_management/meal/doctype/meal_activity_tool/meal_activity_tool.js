// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('MEAL Activity Tool', {
	setup: function(frm) {
		// frm.add_fetch("assessment_plan", "student_group", "student_group");
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			// frm.set_value("student_group", frappe.route_options.student_group);
			// frm.set_value("assessment_plan", frappe.route_options.assessment_plan);
			frappe.route_options = null;
		} else {
			// frm.trigger("assessment_plan");
		}
		frm.disable_save();
		// frm.page.clear_indicator();
	},

	project: function(frm) {
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api_meal_activity_tool.get_indicators",
				args: {
					"project": frm.doc.project					
				},
				callback: function(r) {
					if (r.message) {
						frm.doc.pro_act_list = r.message;
						frm.events.render_table(frm);
						for (let value of r.message) {
							if (!value.docstatus) {
								frm.doc.show_submit = true;
								break;
							}
						}
						// frm.events.submit_result(frm);
					}
				}
			});
		}
	},

	render_table: function(frm) {
		$(frm.fields_dict.meal_activity_html.wrapper).empty();
			frm.events.get_marks(frm);
	},

	get_marks: function(frm) {

		console.log(frm.doc.pro_act_list)
		var meal_activity_table = $(frappe.render_template('meal_activity_tool', {
			frm: frm,
			pro_act_list: frm.doc.pro_act_list
		}));
		meal_activity_table.appendTo(frm.fields_dict.meal_activity_html.wrapper);

	},

	
});
