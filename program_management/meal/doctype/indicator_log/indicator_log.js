// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Indicator Log',
{
	refresh(frm) {
		cur_frm.set_query("indicator", function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return{
				filters: [
				
					['Indicators', 'project_proposal', '=', d.project_proposal],
					
				]
					}
			});

		cur_frm.set_query("governorate", "achieved_indicators", function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		return{
			filters: [
				
				['Territory', 'is_Group', '=', 1],
			
			]
		}
	});    
		cur_frm.set_query("district", "achieved_indicators", function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return{
				filters: [
					
					['Territory', 'parent_territory', '=', d.governorate],
				
				]
			}
		});

		var doc = frm.doc;
		if(!frm.doc.__islocal) {

			frm.add_custom_button(__("Get Indicators"), function() {
			    frappe.call({
        			"method": "frappe.client.get",
        			args: {
        				doctype: "Indicator Log",
        				name: frm.doc.name
        			},
        			callback: function(data){
        				let indicator_detail = data.message.indicator_log_detail;
        				for (var i in indicator_detail) {
        					var new_row =frm.add_child("achieved_indicators");
        					new_row.governorate = indicator_detail[i].governorate;
        					new_row.district = indicator_detail[i].district;
        					new_row.category = indicator_detail[i].category;
        					new_row.type = indicator_detail[i].type;
        					new_row.age_group = indicator_detail[i].age_group;
        				}
        				frm.refresh();
        			}
        		});
			});
		}
		
	},
	
	indicator: function(frm) {
       

		frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Indicators",
				name: frm.doc.indicator
			},
			callback: function(data){
				frm.fields_dict.indicator_log_detail.grid.remove_all();
				let indicator_detail = data.message.indicator_detail;
				for (var i in indicator_detail) {
					frm.add_child("indicator_log_detail");
					frm.fields_dict.indicator_log_detail.get_value()[i].governorate = indicator_detail[i].governorate;
					frm.fields_dict.indicator_log_detail.get_value()[i].district = indicator_detail[i].district;
					frm.fields_dict.indicator_log_detail.get_value()[i].category = indicator_detail[i].category;
					frm.fields_dict.indicator_log_detail.get_value()[i].type = indicator_detail[i].type;
					frm.fields_dict.indicator_log_detail.get_value()[i].age_group = indicator_detail[i].age_group;
					frm.fields_dict.indicator_log_detail.get_value()[i].men = indicator_detail[i].men;
					frm.fields_dict.indicator_log_detail.get_value()[i].women = indicator_detail[i].women;
					frm.fields_dict.indicator_log_detail.get_value()[i].boys = indicator_detail[i].boys;
					frm.fields_dict.indicator_log_detail.get_value()[i].girls = indicator_detail[i].girls;
					frm.fields_dict.indicator_log_detail.get_value()[i].unclassified = indicator_detail[i].unclassified;
					frm.fields_dict.indicator_log_detail.get_value()[i].total = indicator_detail[i].total;
					frm.fields_dict.indicator_log_detail.get_value()[i].verification_method = indicator_detail[i].verification_method;
					frm.fields_dict.indicator_log_detail.get_value()[i].hhs = indicator_detail[i].hhs;
				}
				frm.refresh();
				grid_row.toggle_editable("indicator_log_detail", 0);
			}
		});

	},

	validate: function(frm) {
		if (frm.doc.achieved_indicators){
			cur_frm.cscript.calculate_totals(frm);
		}
		
        frm.trigger("calculate_finald")
		frm.trigger("cumulative_progress")
		
    },
    total_achieved: function(frm) {
        frm.trigger("calculate_finald")
    },
    total: function(frm) {
        frm.trigger("cumulative_progress")
    },
    
    calculate_finald: function(frm) {
        if (frm.doc.total && frm.doc.total_achieved){

			if (frm.doc.is_cumulative == 1){
				var total_achieved = flt(frm.doc.total_achieved/(frm.doc.achieved_indicators.length));
				var mo = frm.doc.months_no;
				if (mo == 0)
					mo = 1;
					
				var cumulative_progress = frm.doc.total_achieved / (frm.doc.total * frm.doc.months_no) * 100
				var remaining = frm.doc.total - self.total_achieved
				var in_progress = 100 - cumulative_progress

				frm.set_value('cumulative_progress', cumulative_progress);
				frm.set_value('remaining', remaining);
				frm.set_value('in_progress', in_progress);
			}else{
				var rem = frm.doc.total - frm.doc.total_achieved;
				var final = flt(frm.doc.total_achieved / frm.doc.total *100);
				var finald = flt(frm.doc.remaining / frm.doc.total * 100);

				frm.set_value('remaining', rem);
				frm.set_value('cumulative_progress', final);
				frm.set_value('in_progress', finald);
			}		
        }
        
    },

	cumulative_progress: function(frm) {
        if(frm.doc.cumulative_progress <100) {
            frm.set_value("status","Under Achieved");
        }
        else if(frm.doc.cumulative_progress > 100) {
            frm.set_value("status","Over Achieved");
        }
        else if(frm.doc.cumulative_progress == 100) {
            frm.set_value("status","Achieved");
        }
    }
});

frappe.ui.form.on('Achieved Indicators', {
    
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
		u.total = u.unclassified;
    }else{
        var total = u.men +  u.women +  u.boys +  u.girls;
		u.total = total;
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
		var total_x = 0;
        frm.doc.achieved_indicators.forEach(function(d) { 
			total_m += (d.men);
			total_w += (d.women);
			total_b += (d.boys);
			total_g += (d.girls);
			total_u += (d.unclassified)
			total_t += (d.total);
		
		});
		// if (frm.doc.is_percentage){            
        //     total_x=total_u/frm.doc.achieved_indicators.length
		// 	total_t=total_x
        // }
		if (frm.doc.is_percentage){
			let length = frm.doc.indicator_log_detail.length;
			total_m /= length;
			total_w /= length;
			total_b /= length;
			total_g /= length;
			total_u /= length;
			total_t /= length;
		}

        frm.set_value("achieved_men", total_m);
        frm.set_value("achieved_women", total_w);
        frm.set_value("achieved_boys", total_b);
        frm.set_value("achieved_girls", total_g);
        frm.set_value("achieved_unclassified", total_u);
        frm.set_value("total_achieved", total_t);
        refresh_field("achieved_men");
        refresh_field("achieved_women");
        refresh_field("achieved_boys");
        refresh_field("achieved_girls");
        refresh_field("achieved_unclassified");
        refresh_field("total_achieved");
    }


/*frappe.ui.form.on('Indicator Log', {

	indicator: function(frm) {
       

		frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Indicator Log",
				name: frm.doc.indicator
			},
			callback: function(data){
				frm.fields_dict.achieved_indicators.grid.remove_all();
			    //frm.fields_dict.table_name_target.grid.remove_all();
				let indicator_detail = data.message.indicator_detail;
				//let var_name = data.message.table_name_in_template;
				for (var i in indicator_detail) {
				//for (var iic in var_name){    
					frm.add_child("achieved_indicators");
					 //frm.add_child("target_table_name");
					frm.fields_dict.achieved_indicators.get_value()[i].governorate = indicator_detail[i].governorate;
					//frm.fields_dict.target_table_name.get_value()[iic].column_name_in_target_table = var_name[iic].column_name_in_template_table;*/


////////////////////////////////////////////////