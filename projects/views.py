from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import messages
from models import Project, Test, Run
from forms import ProjectForm, TestForm, UserForm 
from django.template import RequestContext

from django.contrib.auth import logout, authenticate, login

def home(request):
    return render_to_response('index.html', {'project_list':  Project.objects.all().order_by('name'), 'login_error': "lol"}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))


"""
PROJECT
"""
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        project = form.save()
        project.save()
        return redirect(details_project, project_id=project.key)
    return render_to_response('project_constructor.html',
                              {'errors': form.errors},
                              context_instance=RequestContext(request))
                             
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        edited_project = form.save()
        project.name = edited_project.name
        project.description = edited_project.description
        project.save()
        return redirect(details_project, project_id=project.key)
    return render_to_response('project_constructor.html',
                              {'errors': form.errors,
                               'project': project},
                              context_instance=RequestContext(request))

def delete_project(request, project_id):
    get_object_or_404(Project, pk=project_id).delete()
    return redirect(home)

def details_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('project_details.html',
                              {'project': project},
                              context_instance=RequestContext(request))


"""
TEST
"""
def create_test(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = TestForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        test = form.save()
        test.project = project
        test.save()
        return redirect(details_project, project_id=project.key)
    return render_to_response('test_constructor.html',
                              {'errors': form.errors,
                               'project': project},
                              context_instance=RequestContext(request))
                             
def edit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    form = TestForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        edited_test = form.save()
        test.name = edited_test.name
        test.description = edited_test.description
        test.save()
        return redirect(details_test, test_id=test.key)
    return render_to_response('test_constructor.html',
                              {'errors': form.errors,
                               'test': test},
                              context_instance=RequestContext(request))

def delete_test(request, test_id):
    c = Test.objects.get(pk=test_id)
    project = c.project
    c.delete()
    return redirect(details_project, project_id = project.key)

def details_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    return render_to_response('test_details.html',
                              {'test': test},
                              context_instance=RequestContext(request))

def delete_run(request, run_id):
    c = Run.objects.get(pk=run_id)
    test = c.test
    c.delete()
    return redirect(details_test, test_id = test.key)

"""
USER
"""
def create_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        user = form.save()
        user.save()
        return redirect(home)
    return render_to_response('user_constructor.html',
                              {'errors': form.errors},
                              context_instance=RequestContext(request))

def edit_user(request, user_id):
    if request.user.is_authenticated():
      form = TestForm(request.POST or None)
      if form.is_valid(): # All validation rules pass
          edited_test = form.save()
          test.name = edited_test.name
          test.description = edited_test.description
          test.save()
          return redirect(details_test, test_id=test.key)
      return render_to_response('test_constructor.html',
                                {'errors': form.errors,
                                 'test': test},
                                context_instance=RequestContext(request))
    else:
        return redirect(home)

def log_out(request):
    logout(request)
    return redirect(home)

def log_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(home)
        else:
            messages.add_message(request, messages.ERROR, 'ERROR: User is not active!')
            return redirect(home)
    else:
        messages.add_message(request, messages.ERROR, 'ERROR: Username or password not valid.')
        return redirect(home)


def delete_user(request, user_id):
    return redirect(home)

def details_user(request, user_id):
    return redirect(home)