"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
 

# # Schema view for API v2
# schema_view_v2 = get_schema_view(
#     title='API v2 Documentation',
#     renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
#     url='http://localhost:8000/api/register/',  # Base URL for API v2
#     authentication_classes=[],  # Ensure this is empty
#     permission_classes=[],  
# )
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
#from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.permissions import AllowAny 


schema_view  = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="APIs for user login",
        #terms_of_service="http://localhost:8000/api/login/",
        terms_of_service="https://www.example.com/terms/",  # Placeholder URL
        contact=openapi.Contact(email="jenansol@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
   
   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('login.urls')),
    path('', include('housekeeper.urls')),
    path('swagger/login/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
    # Swagger UI endpoint
    #path('swagger/register/', schema_view_v2, name='swagger-ui-v2'),  # Swagger UI endpoint
]

