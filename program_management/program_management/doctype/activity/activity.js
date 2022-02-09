frappe.ui.form.on('Activity', {
	setup(frm) {
		cur_frm.set_query("output", function() {			
			return{
				filters: {
					project: frm.doc.project,
					type: frm.doc.linked_with
				}}
			});
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
			op = ['Ultimate Outcome', 'Intermediate Outcome', 'Immediate Outcomes', 'Output'];
			frm.set_df_property('linked_with', 'options', [""].concat(op));
		}	
	},

});


frappe.ui.form.on('Activity',  'validate',  function(frm) {
    if (frm.doc.start_date > frm.doc.end_date) {
        msgprint('End Date can not by be before Start Date');
        validated = false;
    } 
});