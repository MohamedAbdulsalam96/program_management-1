// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Managers Monthly Report', {
	refresh: function(frm) {
		frm.set_df_property("get_activities", "hidden", frm.doc.__islocal ? 1:0);

	},
	get_activity: function(frm){
		frm.events.fill_activity(frm);
	},
	fill_activity: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'fill_activity',
			callback: function(r) {
				if (r.docs[0].report_details){
					frm.save();
					frm.refresh();
				}
			}
		})
	}
});