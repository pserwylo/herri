import json
from django.contrib.auth.models import User
from django.db import connections
from api.models import AttributeModel, Attribute, Weighting
from django.core import serializers
from django.http import HttpResponse


# Create your views here.
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

            new_weighting.attribute = existing_attribute[ 0 ]
            new_weighting.weight = weight

            # this will set the id for new_weighting
            new_weighting.save()

            # add to the list of weightings for the new model
            new_model.weightings.add(new_weighting)

        new_model.save()

        try:
            sql = new_model.get_model_sql()
            cursor = connections['gov2014db'].cursor()
            cursor.execute(sql)

        except Exception as e:
            json_data = "{'error': 'MODEL NOT SAVED TO DATABASE %s'}" % (`e`)

            return HttpResponse(json_data, content_type='application/json')

        return get_attribute_model(request, new_model.id)

    except Exception as e:

        json_data = "{'error': '" + `e` + "'}"
        return HttpResponse(json_data, content_type='application/json')