from django import forms
from models import Project, Test
from django.contrib.auth.models import User
from django.core.validators import validate_email

class ProjectForm(forms.Form):
    name        = forms.CharField(max_length=128, required=True)
    description = forms.CharField(required=True)
    def save(form):
        p = Project()
        p.name = form.data.get("name")
        p.description = form.data.get("description")
        return p

class TestForm(forms.Form):
    name        = forms.CharField(max_length=128, required=True)
    description = forms.CharField(required=True)
    def save(form):
        t = Test()
        t.name = form.data.get("name")
        t.description = form.data.get("description")
        return t

class UserForm(forms.Form):
    username    = forms.CharField(max_length=128, required=True)
    email       = forms.EmailField(required=True)
    first_name  = forms.CharField(max_length=128, required=True)
    last_name   = forms.CharField(max_length=128, required=True)
    def save(form):
        u = User()
        u.username   = form.data.get("username")
        u.email      = form.data.get("email")
        u.first_name = form.data.get("first_name")
        u.last_name  = form.data.get("last_name")
        return u

class PasswordForm(forms.Form):
    password    = forms.CharField(min_length=6, max_length=128, required=True)
    def save(form):
        return form.data.get("password")