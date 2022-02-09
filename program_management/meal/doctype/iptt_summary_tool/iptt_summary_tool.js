// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('IPTT Summary Tool', {
	setup: function(frm) {
	},

	refresh: function(frm) {
		if (frappe.route_options) {
			frappe.route_options = null;
		} else {
			// frm.trigger("project");
		}
		frm.disable_save();
		frm.page.clear_indicator();

	},
	project: function(frm) {
		frm.events.get_indicator(frm);
	},
	get_indicator: function(frm){
		frm.doc.show_submit = false;
		if(frm.doc.project) {
			frappe.call({
				method: "program_management.meal.api_iptt_summary.get_project_indicators",
				args: {
					"project": frm.doc.project,		
				},
				freeze:true,
				callback: function(r) {
					$(frm.fields_dict.summary_html.wrapper).empty();
					if (r.message) {
						frm.doc.indicators = r.message;
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
		var table = $(frappe.render_template('iptt_summary_tool', {
			frm: frm,
			indicators: frm.doc.indicators,
		}));
		table.appendTo(frm.fields_dict.summary_html.wrapper);
	
		
	},

});


frappe.ui.form.on('IPTT Summary Tool', {
	project: function(frm) {
		if (frm.doc.percent_complete >= 0 && frm.doc.percent_complete <= 49){
			//frm.set_value("rag", "#CB2929");
			frm.set_df_property('html_5',  'options',  "<div style=\"background:#CB2929; border-radius:5px; height:35px; padding:8px 12px; color:white\"><b> Danger </b></div>");

		}

	    else if (frm.doc.percent_complete >= 50 && frm.doc.percent_complete <= 74){
			//frm.set_value("rag", "#FCF347");
			frm.set_df_property('html_5',  'options',  "<div style=\"background:#FCF347; border-radius:5px; height:35px; padding:8px 12px; color:white\"><b> Warring </b></div>");
		}
		
		 else if (frm.doc.percent_complete >= 75){
			//frm.set_value("rag", "#29CD42");
			frm.set_df_property('html_5',  'options',  "<div style=\"background:#29CD42; border-radius:5px; height:35px; padding:8px 12px; color:white\"><b> Good </b></div>");
		}
	}
});