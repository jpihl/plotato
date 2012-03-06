from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource
from restdata.models import DataSet, DataEntry

class DataSetResource(ModelResource):
    """
    A DataSet has a *name*, *description*, and *unit*, and can be associated with zero or more data entries.
    """
    model = DataSet
    fields = ('created', 'name', 'unit', 'slug', 'description', 'url', 'dataentries', 'project')
    ordering = ('-created',)

    def dataentries(self, instance):
        return reverse('dataentries', kwargs={'dataset': instance.key})

class DataResource(ModelResource):
    """
    A data entry is associated with a given DataSet and has a *revision*, and *value*.
    """
    model = DataEntry
    fields = ('created', 'revision', 'value', 'url', 'dataset')
    ordering = ('-revision','-created',)

    def dataset(self, instance):
        return reverse('dataset', kwargs={'key': instance.dataset.key})
