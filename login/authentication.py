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
from django.contrib.auth import get_user_model

class CustomUserAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type != 'Bearer':
                return None

            if BlacklistedToken.objects.filter(token=token).exists():
                raise AuthenticationFailed('Token has been blacklisted.')

            
            user = self._authenticate_user(token)
            if not user:
                raise AuthenticationFailed('Invalid token.')

            return (user, token)
        except ValueError:
            
            raise AuthenticationFailed('Authorization header must be in the format: Bearer <token>.')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')
        
        
        
        
    def _authenticate_user(self, token):
        try:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
            except:
                refresh_token = RefreshToken(token)
                user_id = refresh_token['user_id']

            # Try to get the user from CustomUser first
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                # If not found, try to get the user from the default Django user model
                User = get_user_model()
                user = User.objects.get(id=user_id)

            return user

        except (CustomUser.DoesNotExist, User.DoesNotExist):
            raise AuthenticationFailed('User not found.')
        except Exception as e:
            raise AuthenticationFailed(f'Error processing token: {str(e)}')

    # def _authenticate_user(self, token):
    #     try:
           
    #         try:
    #             access_token = AccessToken(token)
    #             user_id = access_token['user_id']
    #         except:
               
    #             refresh_token = RefreshToken(token)
    #             user_id = refresh_token['user_id']

    #         user = CustomUser.objects.get(id=user_id)
    #         return user
    #     except CustomUser.DoesNotExist:
    #         raise AuthenticationFailed('User not found.')
    #     except Exception as e:
    #         raise AuthenticationFailed(f'Error processing token: {str(e)}')



###########token#############################################

class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.user_id_field = 'user_id'

    def get_user(self, validated_token):
        try:
            user_id = validated_token[self.user_id_field]
        except KeyError:
            raise InvalidToken(f'Token contained no recognizable {self.user_id_field} claim')

        
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            raise InvalidToken('Invalid UUID format in token')

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
    
    
    
