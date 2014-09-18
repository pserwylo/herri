import os
import csv
import re
from django.contrib.auth.models import User
from django.contrib.gis.utils import LayerMapping
from django.db import connections
from api.models import AttributeModel, Weighting, Attribute

from models import POI, Region


DATA_DIR = os.path.join(os.path.dirname(__file__), '../../db_population/')


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
        os.path.join(DATA_DIR + '/LGAs/filtered/LGA_2011_AUST.shp'))
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


class TableBuilder:
    def __init__(self, csv_path, verbose=True):
        self.csv_path = csv_path
        self.verbose = verbose
        self.cursor = connections['default'].cursor()


    def _attribute_name_to_safe_name(self, attribute_name):
        """
        Makes a string safe to use as a column name in the database.
        Replaces all non alpha numeric characters and replaces them with underscores.
        This includes spaces, apostrophes, and any others.
        """
        return re.sub(r'\W+', '_', attribute_name).lower()


    def _add_required_columns_to_db(self, field_names):
        """
        Given a list of attribute names from table builder, make sure there are relevant
        corresponding columns in the lga_attributes_all table. This will individually
        append the rows to the table. Although it would be just as possible to construct
        a "CREATE TABLE" statement dynamically with these columns and do it faster, and in
        one hit, this is how it is for now. The reason is that when I started writing it,
        the purpose was to augment an existing table with additional fields, not to nuke
        the table and go from scratch. However the limit of 1600 columns in PostgreSQL
        hit, and caused trouble. Thus, we nuke the table and start fresh with only these
        columns.
        :param field_names: Attribute names (human readable, including spaces apostrophes
        etc) from the ABS Table Builder. They will be turned into suitable names for
        database columns using attribute_name_to_safe_name(field_name).
        :return: The field names which were added to the table. Some duplicates appear,
        and so we don't return those twice.
        """
        safe_field_names = [self._attribute_name_to_safe_name(field) for field in field_names]
        added_fields = []
        for field_name in safe_field_names:
            if field_name == 'region_id' or field_name == 'lga_name':
                continue

            if field_name in added_fields:
                if self.verbose:
                    print("Skipping %s, duplicate field" % field_name)
                continue

            if self.verbose:
                print("Adding field %s" % field_name)

            sql_alter = "alter table lga_attributes_all add column %s numeric" % field_name
            self.cursor.execute(sql_alter)
            added_fields.append(field_name)

        return added_fields

    def _ensure_table_exists(self):
        """
        Drops and recreates the lga_attributes_all table. It will not add any columns
        other than "region_id" (which is string representing the LGA code, e.g. "LGA2011").
        These will be added later, as the table builder .csv is parsed and we look at
        the headers of that file.
        :return:
        """
        if self.verbose:
            "Dropping lga_attributes_all and recreating it..."

        self.cursor.execute("DROP TABLE IF EXISTS lga_attributes_all;")
        self.cursor.execute("CREATE TABLE lga_attributes_all ( region_id CHAR(20) PRIMARY KEY, tot_p_p NUMERIC );")

    def _insert_row(self, row_values, fields_to_save):
        if self.verbose:
            print("Inserting row for region %s" % row_values['LGA_NAME'])

        region = None
        try:
            region = Region.objects.get(name=row_values['LGA_NAME'])
        except:
            pass

        if region is None:
            if self.verbose:
                print "Could not find region with name \"%s\"" % row_values['LGA_NAME']
            return

        params = [region.lga_code]
        values = ['%s']
        keys = ['region_id']
        for (key, value) in row_values.items():
            safe_field_name = self._attribute_name_to_safe_name(key)
            if safe_field_name in fields_to_save:
                params.append(value)
                values.append('%s')
                keys.append(safe_field_name)
        sql = "INSERT INTO lga_attributes_all (%s) VALUES (%s)" % (','.join(keys), ','.join(values))
        self.cursor.execute(sql, params)

    def _prepare_total_population(self):
        try:
            # Check if the table exists (it will throw an exception if it doesn't exist)
            self.cursor.execute("SELECT COUNT(*) FROM b01_aust_lga_short")

            self.cursor.execute("UPDATE lga_attributes_all SET tot_p_p = (SELECT b01_aust_lga_short.tot_p_p FROM b01_aust_lga_short WHERE b01_aust_lga_short.region_id = lga_attributes_all.region_id)")
        except:
            db_name = connections['default'].settings_dict['USER']
            db_user = connections['default'].settings_dict['NAME']
            print("ERROR: table b01_aust_lga_short doesn't exist. To create it, from the db_population directory, run:\n\n  psql -w %s %s < b01.sql " % (db_user, db_name))

    def load(self):
        self._ensure_table_exists()

        with open(self.csv_path, 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            fields_to_save = self._add_required_columns_to_db(csv_reader.fieldnames)
            for row in csv_reader:
                self._insert_row(row, fields_to_save)
                # for key, value in row.iteritems():

        self._prepare_total_population()


# TableBuilder(os.path.join(DATA_DIR + '/census-table-builder/Tablebuildercompilation.csv')).load()
# load_lga(True)
create_or_update_autism_model(True)