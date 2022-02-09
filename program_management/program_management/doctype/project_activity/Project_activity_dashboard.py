from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'activity',
		'transactions': [
			{
				'label': _('Action Plan'),
				'items': ['Work Plan Log']
			},
		]
	}