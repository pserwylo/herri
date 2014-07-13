from django.shortcuts import render
from api.models import AttributeModel, Attribute, Weighting
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
def get_attribute_model(request, model_id):

    json_data = serializers.serialize(
        'json'
        , [AttributeModel.objects.get(id=model_id)]
        , relations={'weightings':{'relations':'attribute'}}
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
        
        assert(request.method == 'POST')

        print request.POST

        json_data = request.POST['model']
        python_data = json.loads(json_data)

        new_model = AttributeModel()

        for weighting in python_data['weightings']:

            # create a new weighting
            new_weighting = Weighting()

            # check the attribute exists
            assert(Attribute.objects.exists(weighting['attribute']))

            new_weighting['attribute'] = weighting['attribute']
            new_weighting['weight'] = weighting['weight']

            # this will set the id for new_weighting
            new_weighting.save()

            # add to the list of weightings for the new model
            new_model.weightings.add(new_weighting)

        new_model['description'] = weighting['description']
        new_model['name'] = weighting['name']
        new_model.save()

        return get_attribute_model(request, new_model.id)

    except Exception as e:

        json_data = "{'error': '"+`e`+"'}"

        return HttpResponse(json_data, content_type='application/json')