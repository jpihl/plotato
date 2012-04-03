from django.db import models
import uuid

def uuid_str():
    return str(uuid.uuid1())

class Plot(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    project     = models.ForeignKey('projects.Project', related_name='plots')
    name        = models.CharField(max_length=128)
    description = models.TextField()
    code        = models.TextField('plot code', default='f = figure(figsize=(3,3))')
    created     = models.DateTimeField(auto_now_add=True)
