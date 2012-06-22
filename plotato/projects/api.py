# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from models import Project, Test, Run
from tastyhacks import JSONApiField
from jsonfield import JSONField
from tastypie.fields import CharField
from django.conf import settings

#Authentication answers the question “can they see this data?” 
#Authorization answers the question “what objects can they modify?” 

class PasswordAuthorization(Authorization):
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
            password = request.META.get('HTTP_X_PLOTATO_PASSWORD')

            if not password == settings.ADMIN_PASSWORD:
                return False
            return True

class ProjectResource(ModelResource):
    #Resource for Project()

    class Meta:
        queryset = Project.objects.all()
        list_allowed_methods = ['get']
        authentication = Authentication()
        authorization = PasswordAuthorization()

class TestResource(ModelResource):
    #Resource for Test()

    project = fields.ToOneField(ProjectResource, 'project')

    class Meta:
        queryset = Test.objects.all()
        list_allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = PasswordAuthorization()

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

    class Meta:
        queryset = Run.objects.all()
        authentication = Authentication()
        authorization = PasswordAuthorization()
