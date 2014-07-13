from django.contrib import admin
from api.models import Attribute, Weighting, AttributeModel

# Register your models here.
admin.site.register(Attribute)
admin.site.register(Weighting)
admin.site.register(AttributeModel)
