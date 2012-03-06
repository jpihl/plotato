from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from dataman.models import DataSet
from dataman.models import DataEntry
from dataman.forms import DataSetForm

def details(request, dataset_id):
    return render_to_response('dataman/details.html', {'dataset':  DataSet..objects.get(pk=dataset_id)})

def create(resquest):
    # sticks in a POST or renders empty form
    form = DataSetForm(request.POST or None)
    if form.is_valid():
        dataset = form.save()
        
        dataset.save()
        return redirect(index)
    return render_to_response('dataman/create.html',
                              {'dataset_form': form},
                              context_instance=RequestContext(request))

def delete(request, dataset_id):
    DataSet.objects.get(pk=dataset_id).delete()

    return redirect(index)

def delete_entry(request, entry_id):
    DataEntry.objects.get(pk=entry_id).delete()
    
    return redirect(index)

def edit(request, dataset_id):
    dataset = get_object_or_404(DataSet, pk=dataset_id)

    # sticks in a POST or renders empty form
    form = DataSetForm(request.POST or None, instance=dataset)
    if form.is_valid():
        dataset = form.save()

        dataset.save()
        return redirect(index)

    return render_to_response('dataman/edit.html',
                              {'dataset_form': form,
                               'dataset_id': dataset_id},
                                context_instance=RequestContext(request))