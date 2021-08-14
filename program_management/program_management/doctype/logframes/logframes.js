// Copyright (c) 2021, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Logframes', {
	refresh: function(frm) {
		frm.set_query("come_put", function() {
            return {
                filters: {
                    "project_proposal": frm.doc.project_proposal
                }
            };
        });
	},

});


// consol.log(r.message);
// 			    var child = cur_frm.add_child("itt");
//                 frappe.model.set_value(child.doctype, child.name, "item_code", "My Item Code")
//                 cur_frm.refresh_field("items")
// 				if (r.docs[0].activities){
// 					frm.save();
// 		            frm.refresh();
// 				}