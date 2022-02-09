frappe.listview_settings['Project Activity'] = {
	get_indicator: function(doc) {
		var colors = {
			"Open": "orange",
			"Overdue": "red",
			"Pending Review": "orange",
			"Working": "orange",
			"Completed": "green",
			"Cancelled": "dark grey",
			"Template": "blue"
		}
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
	gantt_custom_popup_html: function(ganttobj, project_activity) {
		var html = `<h5><a style="text-decoration:underline"\
			href="/app/project_activity/${ganttobj.id}""> ${ganttobj.name} </a></h5>`;

		if(project_activity.project) html += `<p>Project: ${project_activity.project}</p>`;
		html += `<p>Progress: ${ganttobj.progress}</p>`;

		if(project_activity._assign_list) {
			html += project_activity._assign_list.reduce(
				(html, user) => html + frappe.avatar(user)
			, '');
		}

		return html;
	}

};
