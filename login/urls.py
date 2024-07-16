from django.urls import path,include
from .views import RegisterView, LoginView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),]
#     path('swagger/', schema_view),
# ]
