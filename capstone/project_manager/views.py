from django.shortcuts import render, redirect

from django.template import loader
from django.http import HttpResponseRedirect
# from .. import settings
from authlib.integrations.django_client import OAuth
# from .secret import client_secret, redirect_uri
from .forms import ProjectForm, TodoListForm
from .models import Project, TodoList



oauth = OAuth()

#################### AUTH ROUTES ####################

 #register a remote application on the OAuth registry via oauth.register method
oauth.register(
    name='basecamp',
    client_id='fdfcd31459e0e7491296ea11a0dd53ab984e3417',
    client_secret='3be318f63a3047d55fcb84d22959a6c6f77e62f2',
    access_token_url='https://launchpad.37signals.com/authorization/token',
    access_token_params=None,
    authorize_url='https://launchpad.37signals.com/authorization/',
    authorize_params=None,
    api_base_url='https://3.basecampapi.com/999999999/',
    client_kwargs={'scope': 'user:email'}, #####################
)

oauth.register(
    name='google',
    client_id='290854060236-8ndifme2eqvjsk04qr4409a7hicgkg08.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://launchpad.37signals.com/authorization/token',
    access_token_params=None,
    authorize_url='https://launchpad.37signals.com/authorization/',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/calendar/v3',
    client_kwargs={'scope': 'user:email'}, ####################
)
# The configuration of those parameters can be loaded from the framework configuration. Each framework has its own config system, read the framework specified documentation later.

# The client_kwargs is a dict configuration to pass extra parameters to OAuth 2 Session, you can pass extra parameters like:

# client_kwargs = {
#     'scope': 'profile',
#     'token_endpoint_auth_method': 'client_secret_basic',
#     'token_placement': 'header',
# }

#You can access the remote application with:
# basecamp = oauth.create_client('basecamp')
# or simply with
# basecamp = oauth.basecamp


# After configuring the OAuth registry and the remote application, the rest steps are much simpler. The only required parts are routes:

# redirect to 3rd party provider (Basecamp) for authentication

# redirect back to your website to fetch access token and profile

# Here is the example for Basecamp login:

def login(request):
    basecamp = oauth.create_client('basecamp')
    redirect_uri = 'http://localhost:8000/token' #### global, don't need to set here?????
    return basecamp.authorize_redirect(request, redirect_uri)

def authorize(request):
    token = oauth.basecamp.authorize_access_token(request)
    resp = oauth.basecamp.get('user', token=token)
    resp.raise_for_status()
    profile = resp.json()
    print(token)
    print('*******************************')
    # do something with the token and profile
    #store token in db? Register with user profile???
    return redirect('projects')
# After user confirmed on Basecamp authorization page, it will redirect back to your website authorize. In this route, you can get your user’s GitHub profile information, you can store the user information in your database, mark your user as logged in and etc.

def welcome(request):
    return render(request, 'project/index.html')

################### PROJECT VIEWS ################### 

def all_projects(request):
    '''Show all my projects with a form to add projects and handle add project form.'''
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save() #saves data to db
            return redirect('all_projects')
    
    else:
        form = ProjectForm()
    return render(request, 'project/projects.html', {'projects': projects, 'form': form})

def project(request, id):
    project = Project.objects.get(pk=id)
    todos = TodoList.objects
    if request.method == 'POST':
        form = TodoListForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('detail')
    return render(request, 'project/detail.html', {'project':project, 'todos': todos})

# def 

############################ LOGIN/SIGNUP VIEWS ############################ 
#Go with User model/form

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save() #saves data to db
            return redirect('login')
    
    else:
        form = UserForm()

    return render(request, 'user/signup.html', {'form': form})

# def login(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)

#         if form.is_valid():
#             return redirect('index')
    
#     else:
#         form = UserForm()
    
#     return render(request, 'user/login.html', {'form': form})

################## BASECAMP REQUESTS ################## 

# @app.get('/buckets/<int:project_id>/todosets/<int:todo_set_id>/todolists.json')
# def get_todo_lists(project_id, todo_set_id): #do I need request in here???????????/
#     """Return a paginated list of active to-do lists in the project with an ID of 1 and the to-do set with ID of 3.
# To get the to-do set ID for a project, see the Get to-do set endpoint."""
#     response = 'hello'
#     return response

# @app.get('/buckets/1/todosets/<int:todo_set_id>.json')
# def get_todo_set(todo_set_id):
#     #Return the to-do set for the project with an ID of 1 and a to-do set ID of 2.
# #To get the to-do set ID for a project, see the Get a project endpoint's dock payload. To retrieve its to-do lists, see the Get to-do lists endpoint.
#     return print('whoaaaa')