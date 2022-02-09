// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt


frappe.ui.form.on('IPTT Logs', {
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


		frm.set_query("governorate", function() {
            return {
				query:"program_management.program_management.doctype.indicators.indicators.get_governorate",
				filters: {'parent': frm.doc.project, 'type':'Project'}
			}
        });
		cur_frm.set_query("indicator", function() {			
			return{
				filters: {
					project: frm.doc.project
				}}
			});    
	},

	project: function(frm) {
		frm.events.get_indicator(frm);
	},
	indicator: function(frm) {
		frm.events.get_indicator(frm);
	},
	end_date: function(frm) {
		frm.events.get_indicator(frm);
	},
	governorate: function(frm) {
		frm.events.get_indicator(frm);
	},
	district: function(frm) {
		frm.events.get_indicator(frm);
	},

	get_indicator: function(frm){
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api_indicator_log.get_project_indicators",
				args: {
					"project": frm.doc.project,
					"indicator": frm.doc.indicator,				
					"start_date": frm.doc.start_date,			
					"end_date": frm.doc.end_date,			
					"governorate": frm.doc.governorate,			
					"district": frm.doc.district,			
				},
				freeze:true,
				callback: function(r) {
					$(frm.fields_dict.logs_html.wrapper).empty();
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
		frm.events.get_marks(frm);
	},

	get_marks: function(frm) {
		var y = {"en" : 99, "aa": 11}
		console.log("get_marks");
		var table = $(frappe.render_template('iptt_logs', {
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
			let date = $input.data().date;
			let gender = $input.data().gender;
			let value = $input.val();

			if(value < 0) {
				$input.val(0);
				value = 0;
			}
			// date = frappe.datetime.str_to_obj(date);
			// d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
			let indicators = [{'indicator': $input.data().indicator, 'ind_detail': ind_detail, 
			'date':date, 'month':month, 'gender':gender, 'value': value}];
			console.log(indicators);
			
			var td = $(this).closest('tr').find('.total');
			var total = 0;
			$(this).closest('tr').find('input').each(function() {
				total += parseInt($(this).val(), 10);
			});
			
			console.log(td);
			frappe.call({
				method: "program_management.meal.api_indicator_log.make_indicator_doc",
				args: {
					"indicators": indicators
				},
				callback: function(r) {
					td.text(total)
				}
			});
		});
		
	},

});