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
from tastypie.authentication import Authentication, ApiKeyAuthentication
from models import Project, Test, Run
from tastyhacks import JSONApiField
from jsonfield import JSONField
from tastypie.validation import Validation

from tastypie.fields import CharField
from tastypie.models import ApiKey

#Authentication answers the question “can they see this data?” 
#Authorization answers the question “what objects can they modify?” 

##API KEY:
models.signals.post_save.connect(create_api_key, sender=User)

class ApiKeyAuthorization(Authorization):
    """
    Only allows GET requests and ApiKey Authorized Posts.
    """

    def is_authorized(self, request, object=None):
        """
        Allow any ``GET`` request.
        """
        if request.method == 'GET':
            return True
        else:
            username   = request.META.get('HTTP_X_PLOTATO_USERNAME')
            api_key    = request.META.get('HTTP_X_PLOTATO_APIKEY')
            parent_key = request.GET.get('test')

            print parent_key

            if not username or not api_key:
                return False
            try:
                user = User.objects.get(username=username)
                ApiKey.objects.get(user=user, key=api_key)
            except (User.DoesNotExist, User.MultipleObjectsReturned, ApiKey.DoesNotExist):
                return False

            
            return True

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
        authorization = ApiKeyAuthorization()

    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(owner=request.user)
class TestResource(ModelResource):
    #Resource for Test()

    project = fields.ToOneField(ProjectResource, 'project')

    class Meta:
        queryset = Test.objects.all()
        list_allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = ApiKeyAuthorization()
    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(project__owner=request.user)

class IRunResource(ModelResource):
    """
    ModelResource subclass that handles JSON fields as JSONApiField.
    """
    @classmethod
    def api_field_from_django_field(cls, f, default=CharField):
        """
        Overrides default field handling to support custom JSONApiField.
        """
        if isinstance(f, JSONField):
            return JSONApiField
    
        return super(IRunResource, cls).api_field_from_django_field(f, default)

class RunResource(IRunResource):
    #Resource for Run()
    test = fields.ToOneField(TestResource, 'test')
    
    #http://stackoverflow.com/questions/7149866/send-an-authenticated-post-request-to-tastypie

    class Meta:
        queryset = Run.objects.all()
        authentication = Authentication()
        authorization = ApiKeyAuthorization() #CustomApiKeyAuthentication()
        list_allowed_methods = ['get', 'post']

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(project__owner=request.user)
