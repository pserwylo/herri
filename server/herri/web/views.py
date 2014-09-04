import json
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from api.models import Attribute, AttributeModel, ModelResult


def _render_model(request, model_id):

    min_zoom = 3
    default_zoom = 4
    map_bounds = [
        [-9.0, 111.3],
        [-46.0, 159.2]
    ]

    # For now, only deal with specific map restrictions for Victoria
    if hasattr(settings, 'RESTRICT_TO_STATE') and settings.RESTRICT_TO_STATE == 2:
        default_zoom = 6
        min_zoom = 6
        map_bounds = [
            [-40.9, 135.1],
            [-32.1, 153.7]
        ]

    index_model = AttributeModel.objects.get(id=model_id)

    index_model_results = ModelResult.objects.filter(run_id=model_id)
    get_key = lambda item: item.lga_code
    index_model_data = dict((get_key(result), float(result.value)) for result in index_model_results)

    context = {
        'json_index_model_data': json.dumps(index_model_data),
        'index_model': index_model,
        'min_zoom': min_zoom,
        'default_zoom': default_zoom,
        'map_bounds': json.dumps(map_bounds)
    }
    return render(request, "web/model.html", context)


def index(request):
    return _render_model(request, 1)


def model(request, model_id):
    return _render_model(request, model_id)


def model_new(request):
    attributes_json = serializers.serialize(
        'json'
        , Attribute.objects.all()
        , indent=4
    )
    context = {'attributes_json': attributes_json}
    return render(request, "web/model_form.html", context)