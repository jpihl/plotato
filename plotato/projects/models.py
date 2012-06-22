from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
import uuid
import jsonfield

def uuid_str():
    return str(uuid.uuid1())

class Project (models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Test(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128)
    description = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    project     = models.ForeignKey(Project, related_name='tests')
    def __unicode__(self):
        return self.name

class Plot(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128)
    description = models.TextField()
    code        = models.TextField(default='f = figure(figsize=(3,3))')
    created     = models.DateTimeField(auto_now_add=True)
    project     = models.ForeignKey(Project, editable=False, related_name='plots')
    def __unicode__(self):
        return self.name

class Run(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    test        = models.ForeignKey(Test, editable=False, related_name='runs')
    created     = models.DateTimeField(auto_now_add=True)
    data        = jsonfield.JSONField(default=None)

    def __unicode__(self):
        return "Run: " + self.created