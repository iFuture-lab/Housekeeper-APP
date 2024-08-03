from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlacklistedToken
from .models import CustomUser  # Import your custom user model

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
                raise AuthenticationFailed('Token has been blacklisted.')

            # Authenticate user based on token
            user = self._authenticate_user(token)
            if not user:
                raise AuthenticationFailed('Invalid token.')

            return (user, token)
        except Exception as e:
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
            return None
