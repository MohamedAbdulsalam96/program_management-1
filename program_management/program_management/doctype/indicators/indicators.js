// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Indicators', {
    validate(frm) {
        cur_frm.cscript.calculate_totals(frm);
    },
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
		    	['Outcome and Output', 'project', '=', d.project]
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
        var total = u.men +  u.women +  u.boys +  u.girls;
        frappe.model.set_value(u.doctype, u.name, "total", total);
    }
    frm.refresh_fields();
    cur_frm.cscript.calculate_totals(frm);
},

cur_frm.cscript.calculate_totals= function(frm) {
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
        if (frm.doc.is_percentage){            
            total_t=total_t/frm.doc.indicator_detail.length
        }
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
    

frappe.ui.form.on('Indicators', {
    project: function(frm) {
        frm.events.filter_(frm);
    },
    source_of_fund: function(frm) {
        var op = "";
        if (frm.doc.source_of_fund == "IRW"){
            op = ['Impact', 'Outcome', 'Output'];
            frm.set_df_property('linked_with', 'options', [""].concat(op));
        }	
        else if(frm.doc.source_of_fund == "OCHA"){
            op = ['Objective', 'Outcome', 'Output'];
            frm.set_df_property('linked_with', 'options', [""].concat(op));
        }	
        else if(frm.doc.source_of_fund == "GAC"){
            op = ['Ultimate Outcome', 'Immediate Outcomes', 'Intermediate Outcome', 'Output'];
            frm.set_df_property('linked_with', 'options', [""].concat(op));
        }	
    },
    
    linked_with: function(frm) {
        if (frm.doc.linked_with == "Impact" || frm.doc.linked_with == "Objective" || frm.doc.linked_with == "Ultimate Outcome" || frm.doc.linked_with == "Project Goal"){
            // frm.set_value("is_group", 1);
            frm.set_df_property('program', 'hidden', 1);
            frm.set_df_property('program', 'reqd', 0);
            frm.set_df_property('parent_outcome_and_output', 'hidden', 1);
            frm.set_df_property('parent_outcome_and_output', 'reqd', 0);
        }
        else if (frm.doc.linked_with == "Intermediate Outcome" || frm.doc.linked_with == "Immediate Outcomes" || frm.doc.linked_with == "Outcome"){
            // frm.set_value("is_group", 1);
            frm.set_df_property('program', 'hidden', 0);
            frm.set_df_property('program', 'reqd', 1);
            frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
            frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
                
            frm.events.filter_(frm);
        }
    
        else if (frm.doc.linked_with == "Output"){
            // frm.set_value("is_group", 0);
            frm.set_df_property('program', 'hidden', 0);
            frm.set_df_property('program', 'reqd', 1);
            frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
            frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
                
            frm.events.filter_(frm);
        }
            // else if (frm.doc.type == "Outcome" || frm.doc.type == "Output"){
            // 	frm.set_value("is_group", 1);
            // 	frm.set_df_property('program', 'hidden', 0);
            // 	frm.set_df_property('program', 'reqd', 1);
            // 	frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
            // 	frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
    
            // 	frm.events.filter_(frm);
            // }
        else{
            // frm.set_value("is_group", 0);
            frm.set_df_property('program', 'hidden', 0);
            frm.set_df_property('program', 'reqd', 1);
            frm.set_df_property('parent_outcome_and_output', 'hidden', 0);
            frm.set_df_property('parent_outcome_and_output', 'reqd', 1);
        }
    },
    
    // filter_:function(frm){
    //     var fil = {
    //         'project': frm.doc.project,
    //         // 'is_group': 1,
    //     }
    //             // if (frm.doc.type == "Outcome" || frm.doc.type == "Intermediate Outcome")
    //             // 	fil.type = "Impact" || "Objective" || "Ultimate Outcome" || "Project Goal";
    
    //     if (frm.doc.type == "Outcome")
    //         fil.linked_with = "Impact";
    
    //     if (frm.doc.type == "Outcome")
    //         fil.linked_with = "Objective";
                
    //     if (frm.doc.linked_with == "Outcome")
    //         fil.linked_with = "Project Goal";	 	 
                
    //     if (frm.doc.linked_with == "Intermediate Outcome")
    //         fil.linked_with = "Ultimate Outcome"; 
    
    //     if (frm.doc.linked_with == "Immediate Outcomes")
    //         fil.linked_with = "Intermediate Outcome";
    
    //     if (frm.doc.linked_with == "Output")
    //         fil.linked_with = "Immediate Outcomes";	
    
    //     else if (frm.doc.linked_with == "Output")
    //         fil.linked_with = "Outcome";
    
    //     frm.set_query("output", function() {
    //         return {
    //             filters: fil
    //         }
    //     });
    //     }
})    