from django.forms import ModelForm
from projects.plots.models import Plot


class PlotForm(ModelForm):
    class Meta:
        model = Plot
        fields = ("name", "code")