from django import forms
from models import Project, Test
#from django.core.validators import validate_email

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