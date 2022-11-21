from django.shortcuts import render
# from .. import settings
from authlib.integrations.django_client import OAuth
# from ../secret import redirect_uri, client_id, client_secret

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
    client_kwargs={'scope': 'user:email'},
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
    # redirect_uri = redirect_uri #### global, don't need to set here?????
    return basecamp.authorize_redirect(request, redirect_uri)

def authorize(request):
    token = oauth.basecamp.authorize_access_token(request)
    resp = oauth.basecamp.get('user', token=token)
    resp.raise_for_status()
    profile = resp.json()
    # do something with the token and profile
    #store token in db? Register with user profile???
    return '...'
# After user confirmed on Basecamp authorization page, it will redirect back to your website authorize. In this route, you can get your user’s GitHub profile information, you can store the user information in your database, mark your user as logged in and etc.

def welcome(request):
    return render(request, 'project/index.html')

def project(request):
    return render(request, 'project/detail.html')

# def 
