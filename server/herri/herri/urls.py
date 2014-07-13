from django.conf.urls import patterns, include, url

from django.contrib import admin
from web import views

admin.autodiscover()

from api.views import get_attribute_model

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'herri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/attribute_models/new/$', 'api.views.save_attribute_model'),
    url(r'^api/attributes/$', 'api.views.get_attributes'),
    url(r'^api/attribute_models/$', 'api.views.get_attribute_models'),
    url(r'^api/attribute_model/(\d+)/$', 'api.views.get_attribute_model', name='model_id'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^model/(\d+)/$', views.model, name='model'),
    url(r'^model/new$', views.model_new, name='model_new'),
)
