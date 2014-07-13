from django.db import models
from django.contrib.auth.models import User

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
