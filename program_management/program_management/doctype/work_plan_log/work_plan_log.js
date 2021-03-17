// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Plan Log', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Work Plan Log', {
	
	// your code here
validate: function(frm) {
	frm.trigger("calculate_progress")
},
calculate_progress: function(frm) {
	if (frm.doc.progress>0 && frm.doc.progress<100){
		frm.set_value('status', 'Working');
	}
	if (frm.doc.progress>=100){
		frm.set_value('status', 'Completed');
	}
	if (frm.doc.progress<=0){
		frm.set_value('status', 'Open');
	}
},

})