from django import forms
from django.core import validators
from models import Project, Test, Plot

class ProjectForm(forms.ModelForm):
  class Meta:
    model  = Project
    fields = ('name', 'description')
  def getKind(self):
    return "Project"

class TestForm(forms.ModelForm):
  class Meta:
    model = Test
    exclude=('project',)
  def getKind(self):
    return "Test"

class PlotForm(forms.ModelForm):
  class Meta:
    model = Plot
  
  def getKind(self):
    return "Plot"