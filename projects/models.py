from django.db import models
import uuid

def uuid_str():
    return str(uuid.uuid1())

class Project (models.Model):
    key         = models.CharField(primary_key=True, max_length=64, default=uuid_str, editable=False)
    name        = models.CharField(max_length=128)
    description = models.TextField()

    def __unicode__(self):
        return self.name