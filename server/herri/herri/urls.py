from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.decorators.cache import cache_page
from web import views

admin.autodiscover()

from api.views import get_attribute_model, data_gis_region, data_gis_poi, data_model_result

urlpatterns = patterns('',

    url(r'^api/geo/poi$', cache_page(60 * 60 * 24 * 7)(data_gis_poi)),
    url(r'^api/geo/region$',  cache_page(60 * 60 * 24 * 7)(data_gis_region)),

    url(r'^api/model/result/(\d+)/$', data_model_result),

    url(r'^api/attribute_models/new/$', 'api.views.save_attribute_model'),
    url(r'^api/attributes/$', 'api.views.get_attributes'),
    url(r'^api/attribute_models/$', 'api.views.get_attribute_models'),
    url(r'^api/attribute_model/(\d+)/$', 'api.views.get_attribute_model', name='model_id'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^model/(\d+)/$', views.model, name='model'),
    url(r'^model/new$', views.model_new, name='model_new'),
)
