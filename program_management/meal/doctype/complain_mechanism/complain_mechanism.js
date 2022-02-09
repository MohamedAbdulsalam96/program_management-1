// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Complain Mechanism', {
	refresh(frm) {
	cur_frm.set_query("governorate", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
		    
			['Territory', 'is_Group', '=', 1],
		
		]
	}
	})
}
    
});

	cur_frm.set_query("district", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
		    
			['Territory', 'parent_territory', '=', d.governorate],
		
		]
	}
});