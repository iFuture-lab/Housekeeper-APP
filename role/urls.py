from .views import RoleCreateView,PermissionCreateView
from django.urls import path,include


urlpatterns = [
    path('role/', RoleCreateView.as_view(), name='role-list-create'),
    path('permission/', PermissionCreateView.as_view(), name='permission-list-create'),]
    #path('role/<uuid:pk>/', RolePerUserRetrieveUpdateDestroyView.as_view(), name='permission-detail'),
    