from django.forms import ModelForm
from dataman.models import DataSet


class DataSetForm(ModelForm):
    class Meta:
        model = DataSet