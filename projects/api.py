# -*- coding: utf-8 -*-

"""RESTful API implementation

Example:
GET Project() data:
curl -H "Accept: application/json" http://127.0.0.1:8000/api/v1/project

POST Environment() data:
curl --dump-header - -H "Content-Type: application/json" -X POST \
--data '{"name": "Single Core"}' \
http://127.0.0.1:8000/api/v1/environment/

PUT Environment() data:
curl --dump-header - -H "Content-Type: application/json" -X PUT \
--data '{"name": "Quad Core"}' \
http://127.0.0.1:8000/api/v1/environment/2/

DELETE Environment() data:
curl --dump-header - -H "Content-Type: application/json" -X DELETE \
http://127.0.0.1:8000/api/v1/environment/2/

PUT a full result:
curl --dump-header - -H "Content-Type: application/json" -X POST \
--data '{"commitid": "4", "branch": "default", "project": "MyProject",\
"executable": "myexe O3 64bits", "benchmark": "float", "environment": \
"Quad Core", "result_value": 4000, "result": "4000"}' \
http://127.0.0.1:8000/api/v1/benchmark-result/

See http://django-tastypie.readthedocs.org/en/latest/interacting.html
"""
import logging
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from tastypie_nonrel.resources import ModelResource
from tastypie_nonrel import fields

from tastypie.models import create_api_key
from tastypie.authorization import Authorization
from projects.models import (Project, Test, Run)


models.signals.post_save.connect(create_api_key, sender=User)


class UserResource(ModelResource):
    """Resource for Django User()"""
    class Meta:
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'email']
        allowed_methods = ['get']
        excludes = ['email', 'password', 'is_superuser']
        authorization = Authorization()


class ProjectResource(ModelResource):
    """Resource for Project()"""

    class Meta:
        queryset = Project.objects.all()
        authorization = Authorization()


class TestResource(ModelResource):
    """Resource for Test()"""

    project = fields.ToOneField(ProjectResource, 'project')

    class Meta:
        queryset = Test.objects.all()
        authorization = Authorization()


class RunResource(ModelResource):
    """Resource for Run()"""

    test = fields.ToOneField(TestResource, 'test')

    class Meta:
        queryset = Run.objects.all()
        authorization = Authorization()