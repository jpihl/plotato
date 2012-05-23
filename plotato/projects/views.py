from django.shortcuts import render_to_response, get_object_or_404, redirect
from middleware import get_manageable_object_or_404
from django.contrib import messages
from models import Project, Test, Run
from django.contrib.auth.models import User
from forms import ProjectForm, TestForm, UserForm, UserEditForm
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def home(request):
    return render_to_response('index.html', {'project_list':  Project.objects.all().order_by('name')}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))


"""
PROJECT
"""
def details_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('project_details.html',
                              {'project': project},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def create_project(request):
    """
    Create a new Project.
    """
    form = ProjectForm(request.POST or None)
    if form.is_valid(): # owner has been excluded. No more error.
        new_project = form.save(commit=False) # returns unsaved instance
        new_project.owner = request.user
        new_project.save() # real save to DB.

        #messages.add_message(request, messages.SUCCESS, 'The project has been successfully created.')
        return redirect(details_project, project_id=new_project.key)
    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def edit_project(request, project_id):
    """
    Edit Project.
    """
    project = get_manageable_object_or_404(Project, pk=project_id, user = request.user)
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

@login_required(login_url='/')
def delete_project(request, project_id):
    p = get_manageable_object_or_404(Project, pk=project_id,  user = request.user)
    p.delete()

    messages.add_message(request, messages.WARNING, 'Project "{0}" was deleted'.format(p.name))
    return redirect(home)


"""
TEST
"""
def details_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    return render_to_response('test_details.html',
                              {'test': test},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def create_test(request, project_id):
    """
    Create a new Test.
    """
    project = get_manageable_object_or_404(Project, pk=project_id, user = request.user)
    form = TestForm(request.POST or None)
    if form.is_valid(): # owner has been excluded. No more error.
        new_test = form.save(commit=False) # returns unsaved instance
        new_test.project = project
        new_test.save() # real save to DB.
        messages.add_message(request, messages.SUCCESS, 'The test has been successfully created.')
        return redirect(details_project, project_id=project_id)
    return render_to_response('form.html',
                              {'form'    : form,
                               'project' : project},
                              context_instance=RequestContext(request))

@login_required(login_url='/')                          
def edit_test(request, test_id):
    """
    Edit Test.
    """
    test = get_manageable_object_or_404(Test, pk=test_id, user = request.user)
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

@login_required(login_url='/')
def delete_test(request, test_id):
    test = get_manageable_object_or_404(Test, pk=test_id, user = request.user)
    project = test.project
    test.delete()

    messages.add_message(request, messages.WARNING, 'Test "{0}" deleted'.format(test.name))
    return redirect(details_project, project_id = project.key)



@login_required(login_url='/')
def delete_run(request, run_id):
    run = get_manageable_object_or_404(Run, pk=run_id, user = request.user)
    test = run.test
    run.delete()
    messages.add_message(request, messages.WARNING, 'Run deleted')
    return redirect(details_test, test_id = test.key)

"""
USER
"""
def create_user(request):
    """
    Create a new User.
    """
    form = UserForm(request.POST or None)
    if form.is_valid(): # owner has been excluded. No more error.
        new_user = form.save()
        #login(request, user)
        messages.add_message(request, messages.SUCCESS, 'The user has been successfully created.')
        return redirect(home)
    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def edit_user(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
    else:
        form = UserEditForm(instance=user)
    if form.is_valid(): # All validation rules pass
            form.save()
            messages.add_message(request, messages.INFO, 'The user has been successfully modified.')
            return redirect(home)
    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def log_out(request):
    messages.add_message(request, messages.INFO, "You are now logged out.")
    logout(request)
    return redirect(home)

def log_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            login(request, user)
            return redirect(home)
        else:
            messages.add_message(request, messages.ERROR, 'ERROR: User is not active!')
            return redirect(home)
    else:
        messages.add_message(request, messages.ERROR, 'ERROR: Username or password not valid.')
        return redirect(home)

@login_required(login_url='/')
def delete_user(request):
    request.user.delete()
    return redirect(home)

@login_required(login_url='/')
def details_user(request):
    return redirect(home)

