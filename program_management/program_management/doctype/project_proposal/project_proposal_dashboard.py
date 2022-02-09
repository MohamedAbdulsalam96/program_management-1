from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'project_proposal',
		'transactions': [
			{
				'label': _('Project Management'),
				'items': ['Project']
			},
			{
				'label': _('Logical Framework'),
				'items': ['Outcome and Output', 'Indicators', 'Project Activity',]
			},
			{
				'label': _('Plans'),
				'items': ['Work Plan',]
			},
		]
	}
