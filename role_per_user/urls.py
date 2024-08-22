from .views import RolePerUserCreateView,RolePerUserRetrieveUpdateDestroyView, RolePerClientCreateView,RolePerClientRetrieveUpdateDestroyView
from django.urls import path,include


urlpatterns = [
    path('permissions/admin', RolePerUserCreateView.as_view(), name='permission-list-create'),
    path('permissions/admin<uuid:pk>/', RolePerUserRetrieveUpdateDestroyView.as_view(), name='permission-detail'),
    
    path('permissions/clients', RolePerClientCreateView.as_view(), name='permission-list-create-client'),
    path('permissions/clients<uuid:pk>/', RolePerClientRetrieveUpdateDestroyView.as_view(), name='permission-detail-client'),
]