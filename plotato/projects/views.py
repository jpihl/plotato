from django.shortcuts import render_to_response, get_object_or_404, redirect
from middleware import is_authorized, admin_only,HttpResponseReload
from django.contrib import messages
from models import Project, Test, Run, Plot
from forms import ProjectForm, TestForm, PlotForm
from django.template import RequestContext
from django.utils.encoding import iri_to_uri
from django.conf import settings
from django.http import HttpResponse



def home(request):
    return render_to_response('index.html', {'project_list':  Project.objects.all().order_by('name')}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))


def details_project(request, project_id):
    """ Project Details.

    """ 
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('project_details.html',
                              {'project': project},
                              context_instance=RequestContext(request))

@admin_only
def create_project(request):
    """ Create a new Project.

    """
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        new_project = form.save()
        return redirect(details_project, project_id=new_project.key)
    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@admin_only
def edit_project(request, project_id):
    """ Edit Project.

    """
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
    else:
        form = ProjectForm(instance=project)
    if form.is_valid(): # All validation rules pass
            form.save()
            messages.add_message(request, messages.INFO, 'The project has been successfully modified.')
            return redirect(details_project, project_id=project.key)

    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@admin_only
def delete_project(request, project_id):
    """ Delete Project.

    """
    p = get_object_or_404(Project, pk=project_id)
    p.delete()

    messages.add_message(request, messages.WARNING, 'Project "{0}" was deleted.'.format(p.name))
    return redirect(home)


def details_test(request, test_id):
    """ Test Details.

    """
    test = get_object_or_404(Test, pk=test_id)
    return render_to_response('test_details.html',
                              {'test': test},
                              context_instance=RequestContext(request))

@admin_only
def create_test(request, project_id):
    """ Create a new Test.

    """
    project = get_object_or_404(Project, pk=project_id)
    form = TestForm(request.POST or None)
    if form.is_valid():
        new_test = form.save(commit=False) # returns unsaved instance
        new_test.project = project
        new_test.save() # real save to DB.
        messages.add_message(request, messages.SUCCESS, 'The test has been successfully created.')
        return redirect(details_project, project_id=project_id)
    return render_to_response('form.html',
                              {'form'    : form,
                               'project' : project},
                              context_instance=RequestContext(request))

@admin_only
def edit_test(request, test_id):
    """ Edit Test.

    """  
    test = get_object_or_404(Test, pk=test_id)
    if request.method == "POST":
        form = TestForm(request.POST, instance=test)
    else:
        form = TestForm(instance=test)
    if form.is_valid(): # All validation rules pass
            form.save()
            messages.add_message(request, messages.INFO, 'The test has been successfully modified.')
            return redirect(details_test, test_id=test_id)

    return render_to_response('form.html',
                              {'form'    : form,
                               'project' : test.project},
                              context_instance=RequestContext(request))

@admin_only
def delete_test(request, test_id):
    """ Delete Test.

    """ 
    test = get_object_or_404(Test, pk=test_id)
    project = test.project
    test.delete()

    messages.add_message(request, messages.WARNING, 'Test "{0}" deleted.'.format(test.name))
    return redirect(details_project, project_id = project.key)


@admin_only
def delete_run(request, run_id):
    """ Delete Run.

    """ 
    run = get_object_or_404(Run, pk=run_id)
    test = run.test
    run.delete()
    return redirect(details_test, test_id = test.key)

@admin_only
def delete_runs(request, test_id):
    """ Delete Runs.

    """ 
    test = get_object_or_404(Test, pk=test_id)
    runs = test.runs.all()
    messages.add_message(request, messages.WARNING, '{0} run(s) deleted.'.format(len(runs)))
    for run in test.runs.all():
        run.delete()

    return redirect(details_test, test_id = test.key)


def details_plot(request, plot_id):
    """ Plot Details.

    """
    plot = get_object_or_404(Plot, pk=plot_id)
    return render_to_response('plot_details.html',
                             {'plot': plot},
                              context_instance=RequestContext(request))

@admin_only
def create_plot(request, project_id):
    """ Create a new Plot.

    """
    project = get_object_or_404(Project, pk=project_id)
    form = PlotForm(request.POST or None)
    if form.is_valid():
        new_plot = form.save(commit=False) # returns unsaved instance
        new_plot.project = project
        new_plot.save() # real save to DB.
        messages.add_message(request, messages.SUCCESS, 'The plot has been successfully created.')
        return redirect(details_project, project_id=project_id)
    return render_to_response('form.html',
                              {'form'    : form,
                               'project' : project},
                              context_instance=RequestContext(request))

@admin_only
def edit_plot(request, plot_id):
    """ Edit a plot.

    """
    plot = get_object_or_404(Plot, pk=plot_id)
    if request.method == "POST":
        form = PlotForm(request.POST, instance=plot)
    else:
        form = PlotForm(instance=plot)
    if form.is_valid(): # All validation rules pass
        form.save()
        messages.add_message(request, messages.INFO, 'The plot has been successfully modified.')
        return redirect(details_plot, plot_id=plot_id)

    return render_to_response('form.html',
                              {'form'    : form,
                               'project' : plot.project},
                              context_instance=RequestContext(request))

@admin_only
def delete_plot(request, plot_id):
    """ Delete Plot.

    """
    plot = get_object_or_404(Plot, pk=plot_id)
    project = plot.project
    plot.delete()
    
    return redirect(details_project, project_id=project.key)

def refresh_plot(request, plot_id):
    """ refresh Plot.
    
    """
    plot = get_object_or_404(Plot, pk=plot_id)
    plot.refresh()
    plot.save()
    messages.add_message(request, messages.INFO, 'The plot has been refreshed.')
    return HttpResponseReload(request)

def log_out(request):
    try:
        del request.session['is_authorized']
        messages.add_message(request, messages.INFO, "You are now logged out.")
    except KeyError:
        pass

    return HttpResponseReload(request)

def log_in(request):
    password = request.POST['password']
    if password == settings.ADMIN_PASSWORD:

        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

        request.session['is_authorized'] = settings.ADMIN_PASSWORD
        return HttpResponseReload(request)
    else:
        messages.add_message(request, messages.ERROR, 'ERROR: Invalid password.')
        return HttpResponseReload(request)