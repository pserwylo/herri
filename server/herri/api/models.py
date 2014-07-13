from django.db import models
from django.contrib.auth.models import User

SQL_TEMPLATE = 'insert into model_results (%s);'
SQL_TABLE = 'lga_attributes_all'

# Create your models here.
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
        return "Model: %s" % (self.name)   

    def get_model_sql(self):

        sql_strings = []

        for weighting in self.weightings.all():
            column_name = weighting.attribute.column_name
            weight = weighting.weight
            sql_strings.append('%s * %f' % (column_name, weight))
        
        sql_result = 'select %d as model_id, region_id, %s as value from %s' % (
            self.id, '+'.join(sql_strings), SQL_TABLE
        )

        return SQL_TEMPLATE % (sql_result)