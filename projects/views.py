from django.shortcuts import render_to_response, get_object_or_404, redirect
from middleware import get_manageable_object_or_404
from django.contrib import messages
from models import Project, Test, Run
from forms import ProjectForm, TestForm, UserForm, PasswordForm
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def home(request):
    return render_to_response('index.html', {'project_list':  Project.objects.all().order_by('name'), 'login_error': "lol"}, context_instance=RequestContext(request))

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
    form = ProjectForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        project = form.save()
        project.owner = request.user
        project.save()
        return redirect(details_project, project_id=project.key)
        messages.add_message(request, messages.SUCCESS, 'The project has been successfully created.')
    return render_to_response('project_constructor.html',
                              {'errors': form.errors},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def edit_project(request, project_id):
    project = get_manageable_object_or_404(Project, pk=project_id, user = request.user)
    form = ProjectForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        edited_project = form.save()
        project.name = edited_project.name
        project.description = edited_project.description
        project.save()
        messages.add_message(request, messages.INFO, 'The project has been successfully modified.')
        return redirect(details_project, project_id=project.key)
    return render_to_response('project_constructor.html',
                              {'errors': form.errors,
                               'project': project},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def delete_project(request, project_id):
    p = get_manageable_object_or_404(Project, pk=project_id,  user = request.user)
    p.delete()

    messages.add_message(request, messages.WARNING, 'Project "{0}" deleted'.format(p.name))
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
    project = get_manageable_object_or_404(Project, pk=project_id, user = request.user)
    form = TestForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        test = form.save()
        test.project = project
        test.save()
        messages.add_message(request, messages.SUCCESS, 'The test has been successfully created.')
        return redirect(details_project, project_id=project.key)
    return render_to_response('test_constructor.html',
                              {'errors': form.errors,
                               'project': project},
                              context_instance=RequestContext(request))

@login_required(login_url='/')                          
def edit_test(request, test_id):
    test = get_manageable_object_or_404(Test, pk=test_id, user = request.user)
    form = TestForm(request.POST or None)
    if form.is_valid(): # All validation rules pass
        edited_test = form.save()
        test.name = edited_test.name
        test.description = edited_test.description
        test.save()
        messages.add_message(request, messages.INFO, 'The test has been successfully modified.')
        return redirect(details_test, test_id=test.key)
    return render_to_response('test_constructor.html',
                              {'errors': form.errors,
                               'test': test},
                              context_instance=RequestContext(request))

@login_required(login_url='/')
def delete_test(request, test_id):
    t = get_manageable_object_or_404(Test, pk=test_id, user = request.user)
    project = t.project
    t.delete()

    messages.add_message(request, messages.WARNING, 'Test "{0}" deleted'.format(t.name))
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
    userform = UserForm(request.POST or None)
    passform = PasswordForm(request.POST or None)
    if userform.is_valid() and passform.is_valid: # All validation rules pass
        user = userform.save()
        user.set_password(passform.save())
        user.save()
        #login(request, user)
        messages.add_message(request, messages.SUCCESS, 'The user has been successfully created.')
        return redirect(home)
    return render_to_response('user_constructor.html',
                              {'errors': userform.errors},
                              context_instance=RequestContext(request))

#Fix this
@login_required(login_url='/')
def edit_user(request):
    userform = UserForm(request.POST or None)
    if userform.is_valid(): # All validation rules pass
        edited_user = userform.save()
        request.user.username = edited_user.username
        request.user.first_name = edited_user.first_name
        request.user.last_name = edited_user.last_name
        request.user.email = edited_user.email
        
        passform = PasswordForm(request.POST or None)
        if passform.is_valid():
            request.user.set_password(passform.save())

        request.user.save()
        return redirect(home)
    return render_to_response('user_constructor.html',
                             {'user_errors': userform.errors},
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

