import os
from django.contrib.auth.models import User
from django.contrib.gis.utils import LayerMapping
from api.models import AttributeModel, Weighting, Attribute

from models import POI, Region


def load_autism_poi(verbose=True):

    autism_poi_mapping = {
        'name': 'Name',
        'description': 'Descriptio',
        'point': 'POINT'
    }

    autism_shp = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../db_population/Autism/filtered/Aut_support.shp'))

    lm = LayerMapping(POI, autism_shp, autism_poi_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


def load_lga(verbose=True):

    lga_mapping = {
        'name': 'LGA_NAME',
        'lga_code': 'LGA_CODE',
        'state_code': 'STATE_CODE',
        'geometry': 'MULTIPOLYGON'
    }

    lga_shp = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../db_population/LGAs/filtered/LGA_2011_AUST.shp'))
    lm = LayerMapping(Region, lga_shp, lga_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


def create_or_update_autism_model(verbose=True):

    try:
        model = AttributeModel.objects.get(id=1)
        model.delete()
    except:
        pass

    model = AttributeModel()
    model.id = 1
    model.description = "This is a map of population density overlayed with markers marking where autism support groups are located within Victoria."
    model.name = "Autism Support Services"
    model.user = User.objects.get(id=1)
    model.save()

    attr_total_population = Attribute.objects.get(column_name='tot_p_p')

    weighting = Weighting()
    weighting.attribute = attr_total_population
    weighting.weight = 1
    weighting.save()

    model.weightings = ( weighting, )
    model.save()

    model.recalculate_index(verbose)
