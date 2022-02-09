// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Proposal', {
    setup(frm){

    },
    refresh(frm) {
		if (frm.doc.docstatus==1){
				frm.add_custom_button(__("Project"), function () {
					frappe.model.open_mapped_doc({
						method: "program_management.program_management.doctype.project_proposal.project_proposal.make_project",
						frm: frm
					});
				},__('Create'));
				frm.page.set_inner_btn_group_as_primary(__('Create'));

		}	
        
        cur_frm.set_query("governorates", function () {
            return {
            filters: [['is_group', '=', 1]]
         };
        });

        frm.set_query("districts", function () {
            if (frm.doc.governorates){
                var list=[];
                frm.doc.governorates.forEach(function(elment){
                    list.push(elment.governorate);
                });
                return {
                    filters: [['parent_territory', 'in', list]]
                }
           }
        });

        frm.set_query("governorate", "target_group", function(doc, cdt, cdn) {
            if (!frm.doc.governorates){
                return;
            }
            var governorates = []
            frm.doc.governorates.forEach(element => {
                governorates.push(element.governorate);
            });
            console.log(frm.doc.governorates);
            return {
                filters: [
                    ['territory_name', 'in', governorates],
                ]
            }
        }); 

        cur_frm.set_query("district", "target_group", function(doc, cdt, cdn) {
            var u = locals[cdt][cdn];
            if (u.governorate){
                return {
                    filters: [['parent_territory', '=', u.governorate]]
                }
            }
        });

        frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Project Proposal'};

		frm.toggle_display(['contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
	},

    planned_end_date: function(frm){
        if (frm.doc.planned_end_date && frm.doc.planned_start_date){
            frappe.call({
                method: 'erpnext.projects.doctype.project.project.get_diffmonth',
				args:{
					start_date: frm.doc.planned_start_date,
					end_date: frm.doc.planned_end_date
				},
                callback: function(r){
					frm.doc.project_duration = r.message.diffrenet;
                    frm.refresh_fields();

                }
            });
        }
    },
	planned_start_date: function(frm){
        if (frm.doc.planned_end_date && frm.doc.planned_start_date){
            frappe.call({
                method: 'erpnext.projects.doctype.project.project.get_diffmonth',
				args:{
					start_date: frm.doc.planned_start_date,
					end_date: frm.doc.planned_end_date
				},
                callback: function(r){
					frm.doc.project_duration = r.message.diffrenet;
                    frm.refresh_fields();

                }
            });
        }
    },

    // validate: function(frm) {
    //     frm.trigger("calculate_duration")
    // },
    // planned_start_date: function(frm) {
    //     frm.trigger("calculate_duration")
    // },
    // planned_end_date: function(frm) {
    //     frm.trigger("calculate_duration")
    // },
    
    // calculate_duration: function(frm) {
    //     if (frm.doc.planned_start_date && frm.doc.planned_end_date) {
	// 		if (frm.doc.planned_end_date < frm.doc.planned_start_date){
	// 		frappe.msgprint(__('planned End Date must be after Planned Start Date'));
	// 		frappe.model.set_value(frm.doctype,frm.docname, 'planned_end_date', '');
	// 	}
	// 	else {
	// 		let age_str = get_age(frm);
	// 		frm.set_value('project_duration', age_str);
	// 	}
	// }
	
    // },
	
});


// let get_age = function (frm) {
// 	let ageMS = Date.parse(frm.doc.planned_end_date) - Date.parse(frm.doc.planned_start_date);
// 	let age = new Date();
// 	age.setTime(ageMS);
// 	let years = age.getFullYear() - 1970;
// 	return years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
// };



frappe.ui.form.on('Target Group', {
    
    target_group_remove: function(frm, cdt, cdn) {
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

cur_frm.cscript.calculate_totals= function(frm, cdt, cdn) {
        var total_m = 0;
        var total_w = 0;
        var total_b = 0;
        var total_g = 0;
        var total_u = 0;
        var with_disability = 0;
        var without_disability = 0;
        frm.doc.target_group.forEach(function(d) { 
            total_m += (d.men); total_w += (d.women); total_b += (d.boys); total_g += (d.girls); total_u += (d.unclassified); 

            if (d.disability == 'With')
                with_disability += (d.total)
            else
                without_disability += (d.total);
        
        });
        frm.set_value("total_men", total_m);
        frm.set_value("total_women", total_w);
        frm.set_value("total_boys", total_b);
        frm.set_value("total_girls", total_g);
        frm.set_value("total_unclassified", total_u);
        frm.set_value("with_disability", with_disability);
        frm.set_value("without_disability", without_disability);
        frm.set_value("total", (with_disability + without_disability));
        frm.refresh();
    }
      