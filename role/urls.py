from .views import RoleCreateView
from django.urls import path,include


urlpatterns = [
    path('role/', RoleCreateView.as_view(), name='role-list-create'),]
    #path('role/<uuid:pk>/', RolePerUserRetrieveUpdateDestroyView.as_view(), name='permission-detail'),
    