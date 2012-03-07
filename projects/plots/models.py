from django.db import models

class Plot(models.Model):
    project = models.ForeignKey('projects.Project', related_name='plots')
    name    = models.CharField(max_length=128)
    code    = models.TextField('plot code', default='f = figure(figsize=(3,3))')