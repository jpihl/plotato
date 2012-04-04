from django.shortcuts import render_to_response, get_object_or_404, redirect
from plots.models import Plot
from projects.models import Project
from django.template import RequestContext
from plots.forms import PlotForm
from django.http import HttpResponse

import matplotlib.pyplot
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import os


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

def create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = PlotForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        plot = form.save()
        plot.project = project
        plot.save()
        #ugly quick fix
        return redirect("/project/details/"+project.key)
    return render_to_response('plot_constructor.html',
                             {'project': project,
                              'errors': form.errors},
                               context_instance=RequestContext(request))

def edit(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
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

def delete(request, plot_id):
    c = Plot.objects.get(pk=plot_id)
    project = c.project
    c.delete()
    #Ugly quick fix
    return redirect("/project/details/"+project.key)

def details(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    return render_to_response('plot_details.html',
                             {'plot': plot},
                              context_instance=RequestContext(request))