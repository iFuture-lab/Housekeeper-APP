from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import CustomUser
# from .models import User 

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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
from django.http import JsonResponse
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
from .serializers import PasswordResetSerializer
from .serializers import PasswordResetRequestSerializer
from django.core.mail import send_mail


from django.contrib.auth import views as auth_views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_summary="Request a password reset email",
    responses={200: "Password reset email sent"}
)
@api_view(['POST'])
def custom_password_reset(request):
    """
    Request a password reset email.
    This endpoint allows users to request a password reset by providing their email address.
    """
    return auth_views.PasswordResetView.as_view()(request)

@swagger_auto_schema(
    method='post',
    operation_summary="Confirm the password reset",
    responses={200: "Password has been reset"}
)
@api_view(['POST'])
def custom_password_reset_confirm(request, uidb64, token):
    """
    Confirm the password reset with a token and set a new password.
    This endpoint allows users to reset their password by providing a valid token and new password.
    """
    return auth_views.PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)





class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        # Generate password reset token
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password/?token={token}&uid={uid}"
            
            # Send email (you need to configure your email backend)
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        
        return Response({"message": "Password reset email sent if the email is registered."}, status=status.HTTP_200_OK)



class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        # Decode the user ID
        try:
            uid = force_text(urlsafe_base64_decode(request.query_params.get('uid')))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        

        
        
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


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializercustomer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=RegisterSerializercustomer,
        responses={
            201: openapi.Response('User created successfully', RegisterSerializercustomer),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
   


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
            return Response({
                'phone_number': user.phone_number,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=400)
        
        
        
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
        return Response({
            'username':user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            # 'role':user.role,
        })
    
    # @swagger_auto_schema(
    #     request_body=LoginSerializer,
    #     responses={
    #         200: openapi.Response('Login successful', openapi.Schema(
    #             type=openapi.TYPE_OBJECT,
    #             properties={
    #                 'username': openapi.Schema(type=openapi.TYPE_STRING),
    #                 'refresh': openapi.Schema(type=openapi.TYPE_STRING),
    #                 'access': openapi.Schema(type=openapi.TYPE_STRING),
    #             }
    #         )),
    #         400: "Invalid credentials"
    #     }
    # )
    

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = authenticate(email=serializer.data['email'],username=serializer.data['username'], password=serializer.data['password'])
    #     email= serializer.data['email']
    #     username= serializer.data['username']
        
     
        
    #     if user is not None:
    #         refresh = RefreshToken.for_user(user)
    #         return Response({
    #             'username': username,
    #             'email':email,
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token),
    #         })
    #     else:
    #         return Response({"detail": "Invalid credentials"}, status=400)