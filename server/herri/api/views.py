import hotshot
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connections
from django.utils.cache import patch_cache_control
from api.models import AttributeModel, Attribute, Weighting, POI, Region, ModelResult
from django.core import serializers
from django.http import HttpResponse

# http://stackoverflow.com/questions/3034482/rendering-spatial-data-of-geoqueryset-in-a-custom-view-on-geodjango
from vectorformats.Formats import Django, GeoJSON


def data_model_result(request, run_id):
    results = ModelResult.objects.filter(run_id=int(run_id))
    get_key = lambda item: item.lga_code
    data = dict((get_key(result), float(result.value)) for result in results)
    return HttpResponse(json.dumps(data), content_type='application/json')


def data_gis_poi(request):
    query_set = POI.objects.all()
    django_format = Django.Django(geodjango="point", properties=['name', 'description'])
    json_data = GeoJSON.GeoJSON().encode(django_format.decode(query_set))

    response = HttpResponse(json_data, content_type='application/json')
    patch_cache_control(response, max_age=3600, public=True)
    return response

def data_gis_region(request):

    def get_float(key, default, min_val, max_val):
        val = float(request.GET.get(key, default))
        if val > max_val:
            val = max_val
        elif val < min_val:
            val = min_val
        return val

    simplification_threshold = get_float('simplification_threshold', '0.5', 0.001, 0.5)
    xmin = get_float('xmin', '110', 110, 170)
    xmax = get_float('xmax', '170', 110, 170)
    ymin = get_float('ymin', '-45', -45, -20)
    ymax = get_float('ymax', '-10', -45, -10)

    bounding_where = " AND geometry && ST_MakeEnvelope( %f, %f, %f, %f ) " % (xmin, ymin, xmax, ymax)

    state_where = ""
    if hasattr(settings, 'RESTRICT_TO_STATE') and settings.RESTRICT_TO_STATE is not None:
        state_where = " AND state_code = %d " % settings.RESTRICT_TO_STATE

    sql = "SELECT id, name, lga_code, ST_Simplify(geometry, %f) AS geometry FROM api_region WHERE TRUE %s %s" % \
          (simplification_threshold, bounding_where, state_where)

    query_set = Region.objects.raw(sql)

    django_format = Django.Django(geodjango="geometry", properties=['name', 'lga_code'])
    django_data = django_format.decode(query_set)
    json_data = GeoJSON.GeoJSON().encode(django_data)

    response = HttpResponse(json_data, content_type='application/json')
    patch_cache_control(response, max_age=3600, public=True)
    return response


def get_attribute_model(request, model_id):
    json_data = serializers.serialize(
        'json'
        , [AttributeModel.objects.get(id=model_id)]
        , relations={'weightings': {'relations': 'attribute'}}
        , indent=4
    )

    return HttpResponse(json_data, content_type='application/json')


def get_attributes(request):
    json_data = serializers.serialize(
        'json'
        , Attribute.objects.all()
        , indent=4
    )

    return HttpResponse(json_data, mimetype='application/json')


def get_attribute_models(request):
    json_data = serializers.serialize(
        'json'
        , AttributeModel.objects.all()
        , indent=4
    )

    return HttpResponse(json_data, content_type='application/json')


def save_attribute_model(request):
    try:

        assert (request.method == 'POST')

        print request.POST

        json_data = request.POST['model']
        python_data = json.loads(json_data)

        new_model = AttributeModel()
        new_model.user = User.objects.get(id=1)
        new_model.description = python_data['description']
        new_model.name = python_data['name']
        new_model.save()

        for weighting in python_data['weightings']:
            # create a new weighting
            new_weighting = Weighting()

            attribute_id = int(weighting['attribute'])
            weight = float(weighting['weight'])

            # check the attribute exists
            existing_attribute = Attribute.objects.filter(id=attribute_id)
            assert (existing_attribute.exists())

            new_weighting.attribute = existing_attribute[0]
            new_weighting.weight = weight

            # this will set the id for new_weighting
            new_weighting.save()

            # add to the list of weightings for the new model
            new_model.weightings.add(new_weighting)

        new_model.save()

        try:
            sql = new_model.get_model_sql()
            cursor = connections['default'].cursor()
            cursor.execute(sql)

        except Exception as e:
            json_data = "{'error': 'MODEL NOT SAVED TO DATABASE %s'}" % (`e`)

            return HttpResponse(json_data, content_type='application/json')

        new_model.recalculate_quantiles()
        new_model.save()

        return get_attribute_model(request, new_model.id)

    except Exception as e:

        json_data = "{'error': '" + `e` + "'}"
        return HttpResponse(json_data, content_type='application/json')
