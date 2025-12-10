from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def validate_google_token(token):
    """
    Verifies a Google ID token.
    """
    try:
        # Load the Client ID from settings
        CLIENT_ID = settings.GOOGLE_OAUTH_CLIENT_ID

        return id_token.verify_oauth2_token(
            token, requests.Request(), audience=CLIENT_ID
        )
    except ValueError as e:
        # This catches "Invalid Token", "Expired Token", or "Wrong Audience"
        raise AuthenticationFailed(f"The token is invalid or expired. Details: {str(e)}")