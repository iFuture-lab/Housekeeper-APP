from django.urls import path,include
from .views import RegisterView, LoginView,home_view,login_view,register_view,LoginViewsystem,RegisterViewsystem,LogoutView,LogoutViewsystem,ResendOtpView
from . views import CustomerBatchView, CustomersListView, DeleteUserView, ResetPasswordView, PasswordResetView, PasswordResetConfirmView,AdminPasswordResetConfirmView,AdminPasswordResetView,VerifyOTPView, TokenValidationView
# urls.py

urlpatterns = [
    path('register/clients', RegisterView.as_view(), name='auth_register_clients'),
    path('delete-account/', DeleteUserView.as_view(), name='delete_account'),
    path('login/clients', LoginView.as_view(), name='auth_login_clients'),
    path('login/token-validate/clients', TokenValidationView.as_view(), name='auth_login_validation'),
    path('logout/clients', LogoutView.as_view(), name='auth_logout_clients'),
    path('register/admin', RegisterViewsystem.as_view(), name='auth_register'),
    path('login/admin', LoginViewsystem.as_view(), name='auth_login'),
    path('logout/admin', LogoutViewsystem.as_view(), name='auth_logout'),
    path('password-reset/clients', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/clients', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/new-password', ResetPasswordView.as_view(), name='new_password'),
    path('password-reset/admin', AdminPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/admin', AdminPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register1/', register_view, name='register'),
    path('login1/', login_view, name='login'),
    path('home/',  home_view, name='home'),
    path('register/verify-otp', VerifyOTPView.as_view(), name='verify-otp'),
    path('register/resend-otp', ResendOtpView.as_view(), name='resend-otp'),
    path('customers/', CustomersListView.as_view(), name='customers'),
    path('customers/batch/', CustomerBatchView.as_view(), name='customers-batch'),
]

