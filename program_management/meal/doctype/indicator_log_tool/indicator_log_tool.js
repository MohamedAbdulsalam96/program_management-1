// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Indicator Log Tool', {
	setup: function(frm) {
		console.log("setup");
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			frappe.route_options = null;
		} else {
			// frm.trigger("project");
		}
		frm.disable_save();
		frm.page.clear_indicator();
		console.log("refresh");
	},

	project: function(frm) {
		console.log("render_table");
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api.get_project_indicators",
				args: {
					"project": frm.doc.project					
				},
				freeze:true,
				callback: function(r) {
					if (r.message) {
						frm.doc.years = r.message[0];
						frm.doc.indicators = r.message[1];
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
		console.log("render_table");
		$(frm.fields_dict.logs_html.wrapper).empty();
		frm.events.get_marks(frm);
	},

	get_marks: function(frm) {
		var y = {"en" : 99, "aa": 11}
		console.log("get_marks");
		var table = $(frappe.render_template('indicator_log_tool', {
			frm: frm,
			indicators: frm.doc.indicators,
			years: frm.doc.years,
		}));
		table.appendTo(frm.fields_dict.logs_html.wrapper);
		
		table.on('change', 'input', function(e) {
			console.log("change");
			let $input = $(e.target);
			let ind_detail = $input.data().detail;
			let month = $input.data().month;
			let value = $input.val();

			if(value < 0) {
				$input.val(0);
			}
			
			let indicators = [{'indicator': $input.data().indicator, 'ind_detail': ind_detail, 'months':{[month]: value}}];
			console.log(indicators);
			
			frappe.call({
				method: "program_management.meal.api.make_indicator_doc",
				args: {
					"indicators": indicators
				},
				callback: function(r) {
					console.log("callback");
				}
			});
		});
		
	},

});
