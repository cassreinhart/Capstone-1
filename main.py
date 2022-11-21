from datetime import datetime, timedelta
from typing import Union, List

from authlib.integrations.django_client import OAuth

import jwt
from pydantic import BaseModel, ValidationError
from passlib.context import CryptContext

from django.http import JsonResponse, HttpResponse
import secret

import requests

import django.contrib.auth.models.User

oauth = OAuth()

oauth.register(
    name='basecamp',
    server_metadata_url='',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

token = oauth.basecamp.authorize_access_token(request)
userinfo = token['userinfo']


ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES= 30

class OAuth2Client(Model, ClientMixin):
    user = ForeignKey(User, on_delete=CASCADE)
    client_id = CharField(max_length=48, unique=True, db_index=True)
    client_secret = CharField(max_length=48, blank=True)
    client_name = CharField(max_length=120)
    redirect_uris = TextField(default='')
    default_redirect_uri = TextField(blank=False, default='')
    scope = TextField(default='')
    response_type = TextField(default='')
    grant_type = TextField(default='')
    token_endpoint_auth_method = CharField(max_length=120, default='')

    # you can add more fields according to your own need
    # check https://tools.ietf.org/html/rfc7591#section-2

    def get_client_id(self):
        return self.client_id

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        allowed = set(scope_to_list(self.scope))
        return list_to_scope([s for s in scope.split() if s in allowed])

    def check_redirect_uri(self, redirect_uri):
        if redirect_uri == self.default_redirect_uri:
            return True
        return redirect_uri in self.redirect_uris

    def has_client_secret(self):
        return bool(self.client_secret)

    def check_client_secret(self, client_secret):
        return self.client_secret == client_secret

    def check_endpoint_auth_method(self, method, endpoint):
        if endpoint == 'token':
          return self.token_endpoint_auth_method == method
        # TODO: developers can update this check method
        return True

    def check_response_type(self, response_type):
        allowed = self.response_type.split()
        return response_type in allowed

    def check_grant_type(self, grant_type):
        allowed = self.grant_type.split()
        return grant_type in allowed



client = OAuth2Client(
    client_id = secret.client_id,
    client_secret = secret.client_secret,
    client_name = "Project Manager",
    redirect_uris = secret.redirect_uri,
    default_redirect_uri =  secret.redirect_uri,
    scope = TextField(default='')
    response_type = TextField(default='')
    grant_type = authorization_code,
    token_endpoint_auth_method = CharField(max_length=120, default='')
)

