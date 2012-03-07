from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from projects.models import Project
from projects.forms import ProjectForm

from dataman.models import DataSet
from projects.plots.models import Plot

def index(request):
    return render_to_response('projects/index.html', {'project_list':  Project.objects.all().order_by('name')})

def create(request):
    # sticks in a POST or renders empty form
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save()
        project.save()

        return redirect(details, project_id=project.key)
    return render_to_response('projects/create.html',
                              {'project_form': form},
                              context_instance=RequestContext(request))
                             
def edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        project = form.save()
        #this is where you might choose to do stuff.
        #project.name = 'test'
        project.save()
        return redirect(details, project_id=project_id)
    return render_to_response('projects/edit.html',
                              {'project_form': form,
                               'project_id': project_id},
                              context_instance=RequestContext(request))
                             
def delete(request, project_id):
    c = Project.objects.get(pk=project_id).delete()
    return redirect(index)

def details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data_sets = DataSet.objects.filter(project=project_id).order_by('name')
    plots = Plot.objects.filter(project=project_id).order_by('name')

    return render_to_response('projects/details.html',
                              {'project': project,
                               'data_sets': data_sets,
                               'plots': plots},
                              context_instance=RequestContext(request))
