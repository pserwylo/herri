import json
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db import connections

SQL_TEMPLATE = 'insert into api_modelresult (run_id, lga_code, value) %s;'
SQL_TABLE = 'lga_attributes_all'


class ModelResult(models.Model):
    run_id = models.IntegerField()
    lga_code = models.CharField(max_length=8)
    value = models.FloatField()

    def __unicode__(self):
        return "Model result for %d" % self.run_id


class POI(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    point = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Region(models.Model):
    """
    Regions represent polygons on the map for which we will colour
    according to the index model. Initially they are only LGA's
    (Local Government Authorities). In the future, it could be more
    detailed (e.g. suburbs) or less detailed (e.g. states).
    """

    lga_code = models.CharField(max_length=8)
    state_code = models.IntegerField()
    name = models.CharField(max_length=50)
    geometry = models.MultiPolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=200)
    column_name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return "Attribute: %s (%s)" % (self.name, self.column_name)


class Weighting(models.Model):
    attribute = models.ForeignKey('Attribute')
    weight = models.FloatField()
    description = models.TextField()

    def __unicode__(self):
        return "Weighting: {0}={1:.2f} ({2})".format('Total pop', 0.913, 1)


class AttributeModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User)
    weightings = models.ManyToManyField('Weighting')

    quantile_0 = models.FloatField(null=True)
    quantile_1 = models.FloatField(null=True)
    quantile_2 = models.FloatField(null=True)
    quantile_3 = models.FloatField(null=True)
    quantile_4 = models.FloatField(null=True)
    quantile_5 = models.FloatField(null=True)

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
            'quantile_0': self.quantile_0,
            'quantile_1': self.quantile_1,
            'quantile_2': self.quantile_2,
            'quantile_3': self.quantile_3,
            'quantile_4': self.quantile_4,
            'quantile_5': self.quantile_5
        })

    def __unicode__(self):
        return "Model: %s" % self.name

    def recalculate_index(self):
        ModelResult.objects.filter(run_id=self.id).delete()

        sql = self.get_model_sql()
        cursor = connections['default'].cursor()
        cursor.execute(sql)

        self._recalculate_quantiles()

    def _recalculate_quantiles(self):
        sql = 'select 0 as id, min(value) as quantile_0, quantile(value, 0.2) as quantile_1, quantile(value, 0.4) as quantile_2, quantile(value, 0.6) as quantile_3, quantile(value, 0.8) as quantile_4, max(value) as quantile_5 from api_modelresult where run_id = %d' % self.id
        query_set = AttributeModel.objects.raw(sql)
        self.quantile_0 = query_set[0].quantile_0
        self.quantile_1 = query_set[0].quantile_1
        self.quantile_2 = query_set[0].quantile_2
        self.quantile_3 = query_set[0].quantile_3
        self.quantile_4 = query_set[0].quantile_4
        self.quantile_5 = query_set[0].quantile_5

    def get_model_sql(self):
        sql_strings = []

        for weighting in self.weightings.all():
            column_name = weighting.attribute.column_name
            weight = weighting.weight
            sql_strings.append('%s * %f' % (column_name, weight))

        state_sql = ''
        state_join_sql = ''
        if hasattr(settings, 'RESTRICT_TO_STATE') and settings.RESTRICT_TO_STATE is not None:
            state_sql = ' and state_code = %d' % int(settings.RESTRICT_TO_STATE)
            state_join_sql = ' join api_region on api_region.lga_code = lga_attributes_all.region_id '

        value_sql = ' ( ' + ' + '.join(sql_strings) + ' ) / tot_p_p '

        sql_result = 'select %d as model_id, region_id, %s as value from lga_attributes_all %s where true %s' % (
            self.id, value_sql, state_join_sql, state_sql
        )

        return SQL_TEMPLATE % sql_result