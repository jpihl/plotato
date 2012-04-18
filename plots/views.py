from django.shortcuts import render_to_response, get_object_or_404, redirect
from projects.middleware import get_manageable_object_or_404
from projects.views import details_project
from plots.models import Plot
from projects.models import Project
from django.template import RequestContext
from plots.forms import PlotForm
from django.http import HttpResponse

import matplotlib.pyplot
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import os

from django.contrib.auth.decorators import login_required

#http://stackoverflow.com/questions/2723842/django-message-framework-and-login-required <--- look into this for messaging user about login requirement

def show(request, plot_id, x_val = 0, y_val = 0):
    plot = get_object_or_404(Plot, pk=plot_id)
    f = figure()
    try:
        exec os.linesep.join(plot.code.splitlines())
    except Exception, e:
        return redirect('http://placehold.it/' + x_val + 'x' + y_val + "&text="+e.args[0])

    matplotlib.pyplot.close(f)
    canvas = FigureCanvasAgg(f)
    if int(x_val) != 0 and int(y_val) != 0:
        f.set_size_inches((float(x_val)/80), (float(y_val)/80))
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

@login_required(login_url='/')
def create(request, project_id):
    project = get_manageable_object_or_404(Project, pk=project_id, user = request.user)
    form = PlotForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        plot = form.save()
        plot.project = project
        plot.save()
        return redirect(details_project, project_id=project.key)
    return render_to_response('plot_constructor.html',
                             {'project': project,
                              'errors': form.errors},
                               context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, plot_id):
    plot = get_manageable_object_or_404(Plot, pk=plot_id, user=request.user)
    form = PlotForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        edited_plot = form.save()
        plot.name = edited_plot.name
        plot.description = edited_plot.description
        plot.code = edited_plot.code
        plot.save()
        return redirect(details, plot_id=plot.key)
    return render_to_response('plot_constructor.html',
                             {'errors': form.errors,
                              'plot':   plot},
                               context_instance=RequestContext(request))

@login_required(login_url='/')
def delete(request, plot_id):
    plot = get_manageable_object_or_404(Plot, pk=plot_id, user=request.user)
    project = plot.project
    plot.delete()
    
    return redirect(details_project, project_id=project.key)

def details(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    return render_to_response('plot_details.html',
                             {'plot': plot},
                              context_instance=RequestContext(request))