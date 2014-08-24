from django.contrib.gis.db import models
from django.contrib.auth.models import User

SQL_TEMPLATE = 'insert into model_results (%s);'
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

    def __unicode__(self):
        return "Model: %s" % self.name

    def get_model_sql(self):
        sql_strings = []

        for weighting in self.weightings.all():
            column_name = weighting.attribute.column_name
            weight = weighting.weight
            sql_strings.append('%s * %f' % (column_name, weight))

        sql_result = 'select %d as model_id, region_id, %s as value from %s' % (
            self.id, '+'.join(sql_strings), SQL_TABLE
        )

        return SQL_TEMPLATE % sql_result