// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Narrative Report', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Narrative Report', {
	refresh: function(frm) {
		//frm.set_df_property("get_activity", "hidden", frm.doc.__islocal ? 1:0);

	},
	get_indicators: function(frm){
		frm.events.fill_indicators(frm);
	},
	fill_indicators: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'fill_indicators',
			callback: function(r) {
				if (r.docs[0].indicator_progress_tracking){
					frm.save();
					frm.refresh();
				}
			}
		})
	}
});
