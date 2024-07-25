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
