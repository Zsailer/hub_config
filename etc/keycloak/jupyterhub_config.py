import os
from jupyterhub.auth import LocalAuthenticator

from oauthenticator.generic import GenericEnvMixin, GenericLoginHandler, GenericOAuthenticator

from traitlets import (
    Unicode
)

KEYCLOAK_HOST = "localhost" 
PORT = 8080
REALM = "master"

def url_from_endpoint(endpoint):
    return f"http://{KEYCLOAK_HOST}:{PORT}/auth/realms/{REALM}/protocol/openid-connect/{endpoint}"


class KeycloakEnvMixin(GenericEnvMixin):
    _OAUTH_ACCESS_TOKEN_URL = url_from_endpoint("token")
    _OAUTH_AUTHORIZE_URL = url_from_endpoint("auth")


class KeycloakLoginHandler(GenericLoginHandler, KeycloakEnvMixin):
    pass


class KeycloakAuthenticator(GenericOAuthenticator):

    login_service = "Keycloak"
    realm = Unicode("master")
    login_handler = KeycloakLoginHandler
    token_url = url_from_endpoint("token")
    userdata_url = url_from_endpoint("userinfo")
    username_key =  "preferred_username"


class LocalKeycloakAuthenticator(LocalAuthenticator, KeycloakAuthenticator):

    """A version that mixes in local system user creation"""
    pass


c.JupyterHub.authenticator_class = LocalKeycloakAuthenticator
c.KeycloakAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'
c.KeycloakAuthenticator.client_id = "jupyterhub"
c.KeycloakAuthenticator.client_secret = ""
