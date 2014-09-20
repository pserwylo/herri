from django import forms
from django.contrib import admin
from django.db import connections, connection
from api.models import Attribute, Weighting, AttributeModel


class AttributeAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):

        # TODO: This is PostgreSQL specific. In the long term, we will need to store the
        # data differently, so that we are not relying on the actual table structure to
        # ascertain what census variables we have access to.
        cursor = connection.cursor()
        cursor.execute("select column_name from information_schema.columns where table_name = 'lga_attributes_all' and column_name not in ('region_id') order by column_name asc;")
        choices = [(row[0], row[0]) for row in cursor.fetchall()]

        column_name_widget = forms.Select(choices=choices)
        kwargs['widgets'] = {
            'column_name': column_name_widget
        }
        return super(AttributeAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Weighting)
admin.site.register(AttributeModel)
