#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "herri.settings")

    from django.core.management import execute_from_command_line

from api.models import AttributeModel

SQL_TEMPLATE = 'insert into model_run (%s);'
SQL_TABLE = 'lga_attributes_all'

def get_model_sql(model_id):

	this_model = AttributeModel.objects.get(id=model_id)

	sql_strings = []

	for weighting in this_model.weightings.all():
		column_name = weighting.attribute.column_name
		weight = weighting.weight
		sql_strings.append('%s * %f' % (column_name, weight))
	
	sql_result = 'select lga_id, %d as model_id, %s as value from %s' % (
		model_id, '+'.join(sql_strings), SQL_TABLE
	)

	return SQL_TEMPLATE % (sql_result)

foo = get_model_sql(1)