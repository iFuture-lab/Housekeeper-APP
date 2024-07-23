from django.urls import path,include
from .views import RegisterView, LoginView,home_view,login_view,register_view,LoginViewsystem,RegisterViewsystem
from . import views
# urls.py

urlpatterns = [
    path('register/clients', RegisterView.as_view(), name='auth_register_clients'),
    path('login/clients', LoginView.as_view(), name='auth_login_clients'),
    path('register/admin', RegisterViewsystem.as_view(), name='auth_register'),
    path('login/admin', LoginViewsystem.as_view(), name='auth_login'),
    path('register1/', register_view, name='register'),
    path('login1/', login_view, name='login'),
    path('home/',  home_view, name='home'),]

