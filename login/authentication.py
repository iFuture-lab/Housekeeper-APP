# authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlacklistedToken, CustomUser

class CustomUserAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type != 'Bearer':
                return None

            # Check if the token is blacklisted
            if BlacklistedToken.objects.filter(token=token).exists():
                print("okaaaaaaaaaaaaaaay")
                raise AuthenticationFailed('Token has been blacklisted.')

            # Authenticate user based on token
            user = self._authenticate_user(token)
            print(user)
            if not user:
                print("my baaaaaaaaaaaaad")
                raise AuthenticationFailed('Invalid token.')

            return (user, token)
        except Exception as e:
            print(f'Authentication error: {str(e)}')
            raise AuthenticationFailed('Invalid token.')

    def _authenticate_user(self, token):
        try:
            refresh_token = RefreshToken(token)
            user_id = refresh_token['user_id']
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
        except Exception as e:
            print(f"Token validation error: {str(e)}")
            return None