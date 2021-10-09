// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Proposal', {
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

frappe.ui.form.on('Project Proposal', {
	refresh: function(frm) {
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Project Proposal'};

		frm.toggle_display(['contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}

	}
});


frappe.ui.form.on('Project Proposal', {
    refresh(frm) {
        
    cur_frm.set_query("governorates", function () {
        return {
        filters: [
            ['Territory', 'is_group', '=', 1],
        ]
    };
});
        frm.set_query("districts", function () {
            if (frm.doc.governorates){
                var list=[];
                frm.doc.governorates.forEach(function(elment){
                    list.push(elment.governorate);
                });
                    return {
            filters: [['Territory', 'parent_territory', 'in', list]]
            }
        
    }

        });
    }
});


frappe.ui.form.on('Project Proposal', {
	
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
});	