// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Proposal', {
    refresh(frm) {
		if (frm.doc.docstatus==1){
			frm.add_custom_button(__("Project"),
				() => frm.events.make_project(frm), __('Create'));
		}		
	},
	make_project: function(frm) {
		frappe.route_options = {"project_proposal": frm.doc.name,
			"project_code": frm.doc.project_no,
			"estimated_costing": frm.doc.budget}
		frappe.set_route("Form", 'Project', 'New Project 1');

	},

    validate: function(frm) {
        frm.trigger("calculate_duration")
    },
    planned_start_date: function(frm) {
        frm.trigger("calculate_duration")
    },
    planned_end_date: function(frm) {
        frm.trigger("calculate_duration")
    },
    
    calculate_duration: function(frm) {
        if (frm.doc.planned_start_date && frm.doc.planned_end_date) {
			if (frm.doc.planned_end_date < frm.doc.planned_start_date){
			frappe.msgprint(__('planned End Date must be after Planned Start Date'));
			frappe.model.set_value(frm.doctype,frm.docname, 'planned_end_date', '');
		}
		else {
			let age_str = get_age(frm);
			frm.set_value('project_duration', age_str);
		}
	}
	
    },
	
});


let get_age = function (frm) {
	let ageMS = Date.parse(frm.doc.planned_end_date) - Date.parse(frm.doc.planned_start_date);
	let age = new Date();
	age.setTime(ageMS);
	let years = age.getFullYear() - 1970;
	return years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
};

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