// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('MEAL Activity', {
	// refresh: function(frm) {
	type: function(frm) {
		if (frm.doc.type == "MEAL Activity"){
			frm.set_value("is_group", 1);
		}
		else if (frm.doc.type == "MEAL Sub-Activity"){
			frm.set_value("is_group", 0);
		}
	// }
	},
});

frappe.ui.form.on('MEAL Activity', {
    refresh(frm) {
	cur_frm.set_query("parent_meal_activity", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
		    
			['MEAL Activity', 'project', '=', d.project],
			['MEAL Activity', 'is_group', '=', 1],

			]
		};
	});
	}	
});


frappe.ui.form.on('MEAL Activity', {
	refresh: function(frm) {
		frm.set_query('main_activity', () => {			
			return{
				filters: {
					project: frm.doc.project
				}
			};
			});
	},	
});

frappe.ui.form.on('MEAL Activity',  'validate',  function(frm) {
    if (frm.doc.start_date > frm.doc.end_date) {
        msgprint('You can not Set End Date Before Start Date');
        validated = false;
    } 
});


frappe.ui.form.on("MEAL Activity", "refresh", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];   
	frappe.model.set_value(cdt, cdn, "duration", frappe.datetime.get_day_diff(d.end_date , d.start_date));
		refresh_field("duration");
	});