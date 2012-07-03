from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
import uuid
import jsonfield
from django.core.files import File

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
from pylab import figure
import os

from plotatoclient import PlotatoClient

from django.conf import settings

from datetime import datetime
import pytz

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

class Run(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    test        = models.ForeignKey(Test, editable=False, related_name='runs')
    created     = models.DateTimeField(auto_now_add=True)
    data        = jsonfield.JSONField(default=None)

    def __unicode__(self):
        return "Run: " + self.created

class Plot(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128)
    description = models.TextField()
    code        = models.TextField(default='fig = figure(figsize=(3,3))')
    error       = models.TextField()
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    project     = models.ForeignKey(Project, editable=False, related_name='plots')
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.refresh()
        super(Plot, self).save(*args, **kwargs)

    def refresh(self):
        fig = figure()
        try:
            ns = {"fig": fig, "PlotatoClient": PlotatoClient, "matplotlib": matplotlib, "figure" : figure}
            code = compile(os.linesep.join(self.code.splitlines()), '<string>', 'exec')
            exec code in ns
        except Exception, e:
            self.error = e.args[0]
            return
        
        fig.savefig(self.full())
        self.error = ""
        return

    def image_url(self):
        # If the plot is older than one hour, update it.
        now = datetime.now(pytz.utc)
        if (now - self.updated).total_seconds() > 3600 or self.error != "" or not os.path.isfile(self.full()):
            self.refresh()
            self.save()

        if self.error != "":
            return "http://placehold.it/800x600&text={0}".format(self.error)
        return "{0}plots/{1}?{2}".format(settings.MEDIA_URL, self.filename(), self.updated)

    def directory(self):
        return os.path.join(settings.MEDIA_ROOT, 'plots')

    def filename(self):
        return "plot-{0}.png".format(self.key)

    def full(self):
        return os.path.join(self.directory(), self.filename())