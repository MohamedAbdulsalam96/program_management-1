frappe.provide("frappe.treeview_settings");

frappe.treeview_settings['Work Plan Log'] = {
	get_tree_nodes: "program_management.program_management.doctype.work_plan_log.work_plan_log.get_children",
	add_tree_node:  "program_management.program_management.doctype.work_plan_log.work_plan_log.add_node",
	filters: [
		{
			fieldname: "work_plan",
			fieldtype:"Link",
			options: "Work Plan",
			label: __("Work Plan"),
		},
		{
			fieldname: "work_plan_log",
			fieldtype:"Link",
			options: "Work Plan Log",
			label: __("Work Plan Log"),
			get_query: function() {
				var me = frappe.treeview_settings['Work Plan Log'];
				var work_plan = me.page.fields_dict.work_plan.get_value();
				var args = [["Work Plan Log", 'is_group', '=', 1]];
				if(work_plan){
					args.push(["Work Plan Log", 'work_plan', "=", work_plan]);
				}
				return {
					filters: args
				};
			}
		}
	],
	breadcrumb: "Program Management",
	get_tree_root: false,
	root_label: "All Work Plan Log",
	ignore_fields: ["parent_work_plan_log"],
	onload: function(me) {
		frappe.treeview_settings['Work Plan Log'].page = {};
		$.extend(frappe.treeview_settings['Work Plan Log'].page, me.page);
		me.make_tree();
	},
	/*toolbar: [
		{
			label:__("Add Multiple"),
			condition: function(node) {
				return node.expandable;
			},
			click: function(node) {
				this.data = [];
				const dialog = new frappe.ui.Dialog({
					title: __("Add Multiple Work Plan Log"),
					fields: [
						{
							fieldname: "multiple_logs", fieldtype: "Table",
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
							method: "program_management.program_management.doctype.work_plan_log.work_plan_log.add_multiple_work_plan_log",
							args: {
								data: dialog.get_values()["multiple_logs"],
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
	],*/
	//extend_toolbar: true
};