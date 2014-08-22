import os
from django.contrib.gis.utils import LayerMapping

from models import POI


autism_poi_mapping = {
    'name': 'Name',
    'description': 'Descriptio',
    'point': 'POINT'
}

autism_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../db_population/Autism/filtered/Aut_support.shp'))


def run(verbose=True):
    lm = LayerMapping(POI, autism_shp, autism_poi_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)