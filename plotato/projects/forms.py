from django import forms
from django.core import validators
from models import Project, Test
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

class ProjectForm(forms.ModelForm):
  class Meta:
    model  = Project
    fields = ('name', 'description')
    exclude=('owner',)
  def getKind(self):
    return "Project"

class TestForm(forms.ModelForm):
  class Meta:
    model = Test
    fields = ('name', 'description')
    exclude=('project',)
  def getKind(self):
    return "Test"

class UserForm(UserCreationForm):
  create_user_code = forms.CharField()

  def getKind(self):
    return "User"

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
  
  def clean(self):
    super(UserForm, self).clean()
    # TODO: This does not work. "not self.Meta.model" returns true for a not-yet created user.
    if self.cleaned_data.get('create_user_code') != settings.CREATE_USER_CODE and not self.Meta.model:
      raise ValidationError('The create user code was invalid.')
    return self.cleaned_data

class UserEditForm(forms.ModelForm):
  def getKind(self):
    return "User"

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')