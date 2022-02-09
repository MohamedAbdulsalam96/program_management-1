frappe.provide("frappe.treeview_settings");

frappe.treeview_settings['Resources'] = {
	get_tree_nodes: "program_management.program_management.doctype.resources.resources.get_children",
	add_tree_node:  "program_management.program_management.doctype.resources.resources.add_node",
	filters: [
		{
			fieldname: "sector",
			fieldtype:"Link",
			options: "Programs",
			label: __("Sector"),
		},
		{
			fieldname: "resources",
			fieldtype:"Link",
			options: "Resources",
			label: __("Resources"),
			get_query: function() {
				var me = frappe.treeview_settings['Resources'];
				var project_proposal = me.page.fields_dict.sector.get_value();
				var args = [["Resources", 'is_group', '=', 1]];
				if(project_proposal){
					args.push(["Resources", 'sector', "=", sector]);
				}
				return {
					filters: args
				};
			}
		}
	],
	breadcrumb: "Program Management",
	get_tree_root: false,
	root_label: "All Resources",
	ignore_fields: ["parent_resources"],
	onload: function(me) {
		frappe.treeview_settings['Resources'].page = {};
		$.extend(frappe.treeview_settings['Resources'].page, me.page);
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
					title: __("Add Multiple Resources"),
					fields: [
						{
							fieldname: "multiple_resources", fieldtype: "Table",
							in_place_edit: true, data: this.data,
							get_data: () => {
								return this.data;
							},
							fields: [{
								fieldtype:'Data',
								fieldname:"resources",
								in_list_view: 1,
								reqd: 1,
								label: __("Resources")
							}]
						},
					],
					primary_action: function() {
						dialog.hide();
						return frappe.call({
							method: "program_management.program_management.doctype.resources.resources.add_multiple_resources",
							args: {
								data: dialog.get_values()["multiple_outputs"],
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
	extend_toolbar: true,
	toolbar: [
		{
            label: __('Download'),
            condition: function(node) {return node.data.attached_file;},
            click: function(node) {
				let a = document.createElement("a");
				a.setAttribute("download", node.data.attached_file.replace("/", "_"));
				a.href = node.data.attached_file;
				a.click();
			},
        },
	],
};