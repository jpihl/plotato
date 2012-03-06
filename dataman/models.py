from django.db import models
from django.template.defaultfilters import slugify
from projects.models import Project
import uuid

def uuid_str():
    return str(uuid.uuid1())

class DataSet(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    project     = models.ForeignKey('projects.Project', related_name='datasets')
    name        = models.CharField(max_length=128)
    description = models.TextField()
    unit        = models.CharField(max_length=128)
    created     = models.DateTimeField(auto_now_add=True)
    slug        = models.SlugField(editable=False, default='')
    def save(self, *args, **kwargs):
        """
        Create a slugified name for browser access.
        """
        self.slug = slugify(self.name)
        super(self.__class__, self).save(*args, **kwargs)

class DataEntry(models.Model):
    dataset     = models.ForeignKey(DataSet, editable=False, related_name='dataentries')
    created     = models.DateTimeField(auto_now_add=True)
    revision    = models.IntegerField()
    value       = models.FloatField()