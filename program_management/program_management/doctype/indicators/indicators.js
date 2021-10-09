// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Indicators', {
	refresh(frm) {
        frm.set_query("governorate", "indicator_detail", function(doc, cdt, cdn) {
            return {
				query:"program_management.program_management.doctype.indicators.indicators.get_governorate",
				filters: {'parent': frm.doc.project_proposal}
			}
        });    
            cur_frm.set_query("district", "indicator_detail", function(doc, cdt, cdn) {
                return {
                    query:"program_management.program_management.doctype.indicators.indicators.get_district",
                    filters: {'parent': frm.doc.project_proposal}
                }
        });

	cur_frm.set_query("output", function(doc, cdt, cdn) {
	    var d = locals[cdt][cdn];
    	return{
	    	filters: [
		    
		    	['Outcome and Output', 'type', '=', d.linked_with],
		    	['Outcome and Output', 'project_proposal', '=', d.project_proposal]
	    	]
            	}
        });

	},
})

frappe.ui.form.on('Indicator Detail', {
    
    indicator_detail_remove: function(frm, cdt, cdn) {
        cur_frm.cscript.calculate_totals(frm);
    },
    men: function(frm, cdt, cdn) {
        cur_frm.cscript.update_row_amount(frm, cdt, cdn)
    },
    women: function(frm, cdt, cdn) {
        cur_frm.cscript.update_row_amount(frm, cdt, cdn)
    },
    boys: function(frm, cdt, cdn) {
        cur_frm.cscript.update_row_amount(frm, cdt, cdn)
    },
    girls: function(frm, cdt, cdn) {
        cur_frm.cscript.update_row_amount(frm, cdt, cdn)
    },
    unclassified: function(frm, cdt, cdn) {
       cur_frm.cscript.update_row_amount(frm, cdt, cdn)
    },
    category: function(frm, cdt, cdn) {
        var u = locals[cdt][cdn];
        frappe.model.set_value(u.doctype, u.name, "men", 0);
        frappe.model.set_value(u.doctype, u.name, "women", 0);
        frappe.model.set_value(u.doctype, u.name, "boys", 0);
        frappe.model.set_value(u.doctype, u.name, "girls", 0);
        frappe.model.set_value(u.doctype, u.name, "unclassified", 0);
        frappe.model.set_value(u.doctype, u.name, "total", 0);
     }
})

cur_frm.cscript.update_row_amount = function(frm, cdt, cdn){
    var u = locals[cdt][cdn];
    
    if(u.is_unclassified == 1){
        frappe.model.set_value(u.doctype, u.name, "total", u.unclassified);
    }else{
        var total = u.men +  u.women +  u.boys +  u.girls +  u.unclassified;
        frappe.model.set_value(u.doctype, u.name, "total", total);
    }
    cur_frm.cscript.calculate_totals(frm);
},

cur_frm.cscript.calculate_totals= function(frm, cdt, cdn) {
        var total_m = 0;
        var total_w = 0;
        var total_b = 0;
        var total_g = 0;
        var total_u = 0;
        var total_t = 0;
        frm.doc.indicator_detail.forEach(function(d) { total_m += (d.men);});
        frm.doc.indicator_detail.forEach(function(d) { total_w += (d.women);});
        frm.doc.indicator_detail.forEach(function(d) { total_b += (d.boys);});
        frm.doc.indicator_detail.forEach(function(d) { total_g += (d.girls);});
        frm.doc.indicator_detail.forEach(function(d) { total_u += (d.unclassified);});
        frm.doc.indicator_detail.forEach(function(d) { total_t += (d.total);});
        frm.set_value("total_men", total_m);
        frm.set_value("total_women", total_w);
        frm.set_value("total_boys", total_b);
        frm.set_value("total_girls", total_g);
        frm.set_value("total_unclassified", total_u);
        frm.set_value("total", total_t);
        refresh_field("total_men");
        refresh_field("total_women");
        refresh_field("total_boys");
        refresh_field("total_girls");
        refresh_field("total_unclassified");
        refresh_field("total");
    }
    