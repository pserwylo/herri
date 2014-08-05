from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings


def index(request):
    context = {'model_id': 1, 'GEOSERVER_URL': settings.GEOSERVER_URL}
    return render(request, "web/model.html", context)


def model(request, model_id):
    context = {'model_id': model_id, 'GEOSERVER_URL': settings.GEOSERVER_URL}
    return render(request, "web/model.html", context)


def model_new(request):
    context = {'GEOSERVER_URL': settings.GEOSERVER_URL}
    return render(request, "web/model_form.html", context)