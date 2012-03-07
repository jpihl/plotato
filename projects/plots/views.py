from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from projects.plots.models import Plot
from projects.plots.forms import PlotForm
from projects.models import Project

import matplotlib.pyplot
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import os

def show(request, project_id, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    f=figure()
    try:
        exec os.linesep.join(plot.code.splitlines())
    except:
        return HttpResponse(status=404)

    matplotlib.pyplot.close(f)
    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def create(request, project_id):
    # sticks in a POST or renders empty form
    form = PlotForm(request.POST or None)
    if form.is_valid():
        plot = Plot(
            project_id = project_id,
            name = form.cleaned_data['name'],
            code = form.cleaned_data['code'],
        )
        plot.save()
        
        return redirect('/details/' + project_id)
    return render_to_response('plots/create.html',
                             {'plot_form': form,
                              'project_id': project_id},
                               context_instance=RequestContext(request))

def delete(request, project_id, plot_id):
    c = Plot.objects.get(pk=plot_id).delete()
    return redirect('/details/' + project_id)

def edit(request, project_id, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    form = PlotForm(request.POST or None, instance=plot)
    if form.is_valid():
        plot = form.save()
        plot.save()
        return redirect('/details/' + project_id)
    return render_to_response('plots/edit.html',
                             {'plot_form': form,
                              'plot_id': plot_id,
                              'project_id': project_id},
                               context_instance=RequestContext(request))