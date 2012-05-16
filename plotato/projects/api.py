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
from tastypie.resources import ModelResource
from tastypie import fields

from tastypie.models import create_api_key
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import Authentication
from models import Project, Test, Run
from tastyhacks import JSONApiField
from jsonfield import JSONField
from tastypie.validation import Validation

from tastypie.fields import CharField

#Authentication answers the question “can they see this data?” 
#Authorization answers the question “what objects can they modify?” 

models.signals.post_save.connect(create_api_key, sender=User)

"""
class UserResource(ModelResource):
    #Resource for Django User()
    class Meta:
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'email']
        allowed_methods = ['get']
        excludes = ['email', 'password', 'is_superuser']
        authorization = Authorization()
"""

class ProjectResource(ModelResource):
    #Resource for Project()

    class Meta:
        queryset = Project.objects.all()
        list_allowed_methods = ['get']
        authentication = Authentication()
        authorization = Authorization()

    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(owner=request.user)
class TestResource(ModelResource):
    #Resource for Test()

    project = fields.ToOneField(ProjectResource, 'project')

    class Meta:
        queryset = Test.objects.all()
        list_allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()
    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(project__owner=request.user)

class IRunResource(ModelResource):
    """
    ModelResource subclass that handles geometry fields as GeoJSON.
    """

    

    @classmethod
    def api_field_from_django_field(cls, f, default=CharField):
        """
        Overrides default field handling to support custom GeometryApiField.
        """
        if isinstance(f, JSONField):
            return JSONApiField
    
        return super(IRunResource, cls).api_field_from_django_field(f, default)

class AwesomeValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Not quite what I had in mind.'}

        errors = {}

        for key, value in bundle.data.items():
            if not isinstance(value, basestring):
                continue

            if not 'awesome' in value:
                errors[key] = ['NOT ENOUGH AWESOME. NEEDS MORE.']

        return errors

class RunResource(IRunResource):
    #Resource for Run()
    test = fields.ToOneField(TestResource, 'test')

    class Meta:
        queryset = Run.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
    
    def dehydrate(self, bundle):
        print "dehydrate"
        return bundle

    def hydrate(self, bundle):
        print "hydrate"
        return bundle

    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(project__owner=request.user)
