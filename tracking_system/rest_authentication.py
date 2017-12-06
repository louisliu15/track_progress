from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import base64
import binascii

HTTP_HEADER_ENCODING = 'iso-8859-1'

class EmailAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = ('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        username, password = auth_parts[0], auth_parts[2]
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
