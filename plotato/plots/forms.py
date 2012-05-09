from django import forms
from models import Plot
#from django.core.validators import validate_email

class PlotForm(forms.Form):
    name        = forms.CharField(max_length=128, required=True)
    code		= forms.CharField(required=True)
    description = forms.CharField(required=True)
    def save(form):
        p = Plot()
        p.name = form.data.get("name")
        p.description = form.data.get("description")
        p.code = form.data.get("code")
        return p