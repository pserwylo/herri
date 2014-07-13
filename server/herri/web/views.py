from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    context = {'model_id': 1}
    return render(request, "web/model.html", context)


def model(request, model_id):
    context = {'model_id', model_id}
    return render(request, "web/model.html", context)


def model_new(request):
    return render(request, "web/model_form.html")