from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from django.db.models.signals import post_save
import uuid

def uuid_str():
    return str(uuid.uuid1())

class Project (models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128, unique = True)
    owner       = models.ForeignKey(User, editable=False, related_name='projects')
    description = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    def user_can_manage_me(self, user):
        return user == self.owner

class Test(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128)
    description = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    slug        = models.SlugField(editable=False, default='')
    project     = models.ForeignKey(Project, editable=False, related_name='tests')
    def __unicode__(self):
        return self.name

    def user_can_manage_me(self, user):
        return user == self.project.owner

    def save(self, *args, **kwargs):
        """
        Create a slugified name for browser access.
        """
        self.slug = slugify(self.name)
        super(self.__class__, self).save(*args, **kwargs)

class Run(models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    test        = models.ForeignKey(Test, editable=False, related_name='runs')
    created     = models.DateTimeField(auto_now_add=True)
    data        = DictField()
    def __unicode__(self):
        return "Run: " + self.created
    def user_can_manage_me(self, user):
        return user == self.test.project.owner