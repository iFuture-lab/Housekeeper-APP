from django.urls import path
from .views import PericePerNationalityRetrieveUpdateDestroyView,PericePerNationalityCreateView


urlpatterns = [
    path('price-per-nationality/', PericePerNationalityCreateView.as_view(), name='perice-list-create'),
    path('price-per-nationality/<uuid:pk>/',PericePerNationalityRetrieveUpdateDestroyView.as_view(), name='perice-retrieve-update-destroy'),
   ]