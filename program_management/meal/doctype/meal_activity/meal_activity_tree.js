frappe.provide("frappe.treeview_settings");

frappe.treeview_settings['MEAL Activity'] = {
	get_tree_nodes: "program_management.meal.doctype.meal_activity.meal_activity.get_children",
	add_tree_node:  "program_management.meal.doctype.meal_activity.meal_activity.add_node",
	filters: [
		{
			fieldname: "project",
			fieldtype:"Link",
			options: "Project",
			label: __("Project"),
		},
		{
			fieldname: "meal_activity",
			fieldtype:"Link",
			options: "MEAL Activity",
			label: __("MEAL Activity"),
			get_query: function() {
				var me = frappe.treeview_settings['MEAL Activity'];
				var project = me.page.fields_dict.project.get_value();
				var args = [["MEAL Activity", 'is_group', '=', 1]];
				if(project){
					args.push(["MEAL Activity", 'project', "=", project]);
				}
				return {
					filters: args
				};
			}
		}
	],
	breadcrumb: "MEAL",
	get_tree_root: false,
	root_label: "All MEAL Activity",
	ignore_fields: ["parent_meal_activity"],
	onload: function(me) {
		frappe.treeview_settings['MEAL Activity'].page = {};
		$.extend(frappe.treeview_settings['MEAL Activity'].page, me.page);
		me.make_tree();
	},
	toolbar: [
		{
			label:__("Add Multiple"),
			condition: function(node) {
				return node.expandable;
			},
			click: function(node) {
				this.data = [];
				const dialog = new frappe.ui.Dialog({
					title: __("Add Multiple MEAL Activity"),
					fields: [
						{
							fieldname: "multiple_activities", fieldtype: "Table",
							in_place_edit: true, data: this.data,
							get_data: () => {
								return this.data;
							},
							fields: [{
								fieldtype:'Data',
								fieldname:"subject",
								in_list_view: 1,
								reqd: 1,
								label: __("Subject")
							}]
						},
					],
					primary_action: function() {
						dialog.hide();
						return frappe.call({
							method: "program_management.meal.doctype.meal_activity.meal_activity.add_multiple_meal_activity",
							args: {
								data: dialog.get_values()["multiple_activities"],
								parent: node.data.value
							},
							callback: function() { }
						});
					},
					primary_action_label: __('Create')
				});
				dialog.show();
			}
		}
	],
	extend_toolbar: true
};