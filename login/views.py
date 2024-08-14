from django.shortcuts import render,redirect
import logging

logger = logging.getLogger(__name__)
#from django.contrib.auth.models import User
from .models import CustomUser
# from .models import User 

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,TokenError,AccessToken
from django.contrib.auth import authenticate,login
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .serializers import RegisterSerializercustomer, LoginSerializercustomer,RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, generics
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from .serializers import PasswordResetSerializer,PasswordResetConfirmSerializer,AdminPasswordResetSerializer, AdminPasswordResetConfirmSerializer
from django.core.mail import send_mail
from rest_framework.views import APIView


from django.contrib.auth import views as auth_views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import BlacklistedToken
from .utils import send_otp, verify_otp,resend_otp

from django.core.cache import cache
from .authentication import CustomJWTAuthentication,CustomUserAuthentication
from role_per_user.models import RolePerClient,RolePerUser

User = get_user_model()


##################password Admin#####################################

class AdminPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset token sent."})

class AdminPasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminPasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."})





################Password Client########################
class PasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        # Here you should send the token to the user's phone number via SMS
        return Response({"detail": "Password reset token sent."}, status=status.HTTP_200_OK)
    
    
class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


        
        
########################### clients views #########################################
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            phone_number = form.cleaned_data.get('phone_number')
           
            password = form.cleaned_data.get('password')
            user = authenticate(phone_number= phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('/api/home')  # Redirect to home page
            else:
                return HttpResponse('Invalid login credentials')
        else:
            return HttpResponse('Invalid form data')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            return HttpResponse('Invalid form data')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# @login_required
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def home_view(request):
    return render(request, 'home.html')



# class RegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializercustomer

#     @swagger_auto_schema(
#         request_body=RegisterSerializercustomer,
#         responses={
#             201: openapi.Response('User created successfully', RegisterSerializercustomer),
#             400: "Bad Request"
#         }
#     )
    
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)
        
        
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializercustomer
    
    
    @swagger_auto_schema(
        operation_description="Register a new user and send an OTP for phone number verification.",
        responses={
            201: openapi.Response("User registered successfully. OTP sent. Please verify the OTP to activate your account.", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )),
            500: openapi.Response("Cannot send OTP.")
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save(is_confirmed=False)  # Create user but keep inactive
        phone_number = user.phone_number
        
        test_mode = request.data.get('test_mode', False)  # Default to False if not provided
        success, otp_or_message = send_otp(phone_number, test_mode=test_mode)
        
        if success:
            # Save OTP and phone number in OTPVerification model
            return Response({
                'message': 'User registered successfully. OTP sent. Please verify the OTP to activate your account.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Delete the user if OTP sending failed
            return Response({
                'message': 'can not send otp'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    
     
        
class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Verify the OTP sent to the user's phone number and complete the registration.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'test_mode': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Set to true to simulate verification without actual OTP validation'),
            },
            required=['otp', 'user_id']
        ),
        responses={
            200: openapi.Response("OTP verified successfully. Registration complete."),
            400: openapi.Response("Invalid OTP. A new OTP has been sent. Please try again."),
            404: openapi.Response("User not found. Please provide a valid user ID.")
        }
    )
    
    def post(self, request, *args, **kwargs):
        entered_otp = request.data.get('otp')
        #phone_number = request.data.get('phone_number') 
        user_id = request.data.get('user_id')
        test_mode = request.data.get('test_mode', False)

        if user_id is None:
            return Response({
                'message': 'User ID not found. Please initiate the OTP process again.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({
                'message': 'User not found. Please initiate the OTP process again.'
            }, status=status.HTTP_404_NOT_FOUND)

        phone_number = user.phone_number  # Use phone number from user object

        if verify_otp(phone_number, entered_otp, test_mode=test_mode):
            user.is_confirmed = True
            user.save()
            return Response({
                'message': 'OTP verified successfully. Registration complete.'
            }, status=status.HTTP_200_OK)
        else:
            # Optionally, you can resend the OTP if it was wrong or expired
            success, message = resend_otp(phone_number, test_mode=test_mode)
            return Response({
                'message': 'Invalid OTP. A new OTP has been sent. Please try again.'
            } if success else {
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
class ResendOtpView(APIView):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Resend the OTP to the user's phone number.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the user to resend OTP to'),
                'test_mode': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Set to true to simulate OTP sending without actually sending it'),
            },
            required=['user_id']
        ),
        responses={
            200: openapi.Response("A new OTP has been sent. Please check your phone."),
            400: openapi.Response("User ID not found. Please provide a valid user ID."),
            404: openapi.Response("User not found. Please provide a valid user ID."),
            500: openapi.Response("Failed to send OTP.")
        }
    )

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')  # Get user ID from request
        test_mode = request.data.get('test_mode', False)  # Default to False if not provided

        if user_id is None:
            return Response({
                'message': 'User ID not found. Please provide a valid user ID.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({
                'message': 'User not found. Please provide a valid user ID.'
            }, status=status.HTTP_404_NOT_FOUND)

        phone_number = user.phone_number  # Use phone number from user object

        success, message = resend_otp(phone_number, test_mode=test_mode)
        if success:
            return Response({
                'message': 'A new OTP has been sent. Please check your phone.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            

class LogoutView(APIView):
    authentication_classes = [CustomUserAuthentication] 
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh_token']
        ),
        responses={
            200: "Logout successful",
            400: "Invalid token or no token provided",
        }
    )
    
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'detail': 'No Authorization header provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_type, access_token = auth_header.split()
            if token_type != 'Bearer':
                return Response({'detail': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)

        # Decode and validate the access token
            token = AccessToken(access_token)
            user_id = str(token['user_id'])

        # Check if the user exists
            if not CustomUser.objects.filter(id=user_id).exists():
                return Response({'detail': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is already blacklisted
            if BlacklistedToken.objects.filter(token=access_token).exists():
                return Response({'detail': 'Token is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the token to the blacklist
            BlacklistedToken.objects.create(token=access_token)
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     refresh_token = request.data.get('refresh_token')
    #     if not refresh_token:
    #         return Response({'detail': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Decode and validate the refresh token
    #         token = RefreshToken(refresh_token)
    #         user_id = str(token['user_id'])  # Ensure user_id is a string

    #         # Check if the user exists
    #         if not CustomUser.objects.filter(id=user_id).exists():
    #             return Response({'detail': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    #         # Check if the token is already blacklisted
    #         if BlacklistedToken.objects.filter(token=refresh_token).exists():
    #             return Response({'detail': 'Token is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

    #         # Add the token to the blacklist
    #         BlacklistedToken.objects.create(token=refresh_token)
    #         return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    
    


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializercustomer
    @swagger_auto_schema(
        request_body=LoginSerializercustomer,
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'user_info':openapi.Schema(type=openapi.TYPE_STRING),
                    'role':openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: "Invalid credentials"
        }
    )
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        # username= serializer.validated_data['']

        user = authenticate(request, phone_number=phone_number,  password=password, backend= 'login.backend.PhoneNumberBackend')

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token   
            access_token.payload.update({
                'user_id': str(user.id)
            })
            
            client_roles = RolePerClient.objects.filter(clients=user).values_list('role', flat=True).first()
            return Response({
                'phone_number': user.phone_number,
                'refresh': str(refresh),
                'access': str(access_token),
                'user_info': {
                    'id': str(user.id),
                    'username': user.fullName,
                    'email': user.email,
                    'nationalID': user.nationalID,
                    'dateOfBirth':user.dateOfBirth,
                    'role':client_roles
                }
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=400)
        
# @authentication_classes([CustomJWTAuthentication])       
class TokenValidationView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: "Token is valid",
            401: "Token is invalid or expired",
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # Token is valid, return user info
            user_info = {
                'id': user.id,
                'username': user.fullName,
                'email': user.email,
                'phone_number':user.phone_number
                # Add other user fields you want to include
            }
            return Response({
                "detail": "Token is valid",
            }, status=200)
        else:
            # Token is invalid or expired
            return Response({"detail": "Token is invalid or expired"}, status=401)
        
        
        
    ###########################################################################################################
    
        

    ############################################ system user ##################################################

class RegisterViewsystem(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User created successfully', RegisterSerializer),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
   


class LoginViewsystem(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )),
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token   
        access_token.payload.update({
                'user_id': user.id
            })
        user_roles = RolePerUser.objects.filter(users=user).values_list('role', flat=True).first()
        return Response({
            'username':user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(access_token),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'role':user_roles
        })
    
    
class LogoutViewsystem(APIView):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh_token']
        ),
        responses={
            200: "Logout successful",
            400: "Invalid token or no token provided",
        }
    )
    
    

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
 
            # Decode the refresh token to get the user
            token = RefreshToken(refresh_token)
            user_id = token.get('user_id')
                
            if not User.objects.filter(id=user_id).exists():
                return Response({'detail': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # # Check if the token is already blacklisted
            #     if BlacklistedToken.objects.filter(token=refresh_token).exists():
            #         return Response({'detail': 'Token is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

            # # Add the token to the blacklist
            #     BlacklistedToken.objects.create(token=refresh_token)
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except TokenError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
             

    

  
     
        
    