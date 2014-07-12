from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Attribute(models.Model):
    name = models.CharField(max_length=200)
    column_name = models.CharField(max_length=200)
    description = models.TextField()

class Weighting(models.Model):
    attribute = models.ForeignKey('Attribute')
    weight = models.FloatField()
    description = models.TextField()

class AttributeModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User)
    weightings = models.ManyToManyField('Weighting')
