from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import BlacklistedToken
from .models import CustomUser  # Import your custom user model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import User as DefaultUser
from .models import CustomUser
import uuid

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

            # Attempt to authenticate using the token
            user = self._authenticate_user(token)
            if not user:
                raise AuthenticationFailed('Invalid token.')

            return (user, token)
        except ValueError:
            # Handle case where Authorization header is malformed
            raise AuthenticationFailed('Authorization header must be in the format: Bearer <token>.')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')

    def _authenticate_user(self, token):
        try:
            # Try AccessToken first
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
            except:
                # Fallback to RefreshToken if AccessToken fails
                refresh_token = RefreshToken(token)
                user_id = refresh_token['user_id']

            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found.')
        except Exception as e:
            raise AuthenticationFailed(f'Error processing token: {str(e)}')



###########token#############################################

class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure this matches the claim used in token creation
        self.user_id_field = 'user_id'

    def get_user(self, validated_token):
        try:
            user_id = validated_token[self.user_id_field]
        except KeyError:
            raise InvalidToken(f'Token contained no recognizable {self.user_id_field} claim')

        # Convert user_id to UUID if necessary
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            raise InvalidToken('Invalid UUID format in token')

        # Check DefaultUser and CustomUser
        try:
            user = DefaultUser.objects.get(id=user_id)
        except DefaultUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed('User not found')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive')

        return user
    
    
    
# class CustomJWTAuthentication(JWTAuthentication):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Ensure this matches the claim used in token creation
#         self.user_id_field = 'user_id'

#     def get_user(self, validated_token):
#         try:
#             user_id = validated_token[self.user_id_field]
#         except KeyError:
#             raise InvalidToken(f'Token contained no recognizable {self.user_id_field} claim')

#         # Check DefaultUser and CustomUser
#         try:
#             user = DefaultUser.objects.get(id=user_id)
#         except DefaultUser.DoesNotExist:
#             try:
#                 user = CustomUser.objects.get(id=user_id)
#             except CustomUser.DoesNotExist:
#                 raise AuthenticationFailed('User not found')

#         if not user.is_active:
#             raise AuthenticationFailed('User is inactive')

#         return user
   