import os
from django.contrib.gis.utils import LayerMapping

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


def __init__():
    load_lga()