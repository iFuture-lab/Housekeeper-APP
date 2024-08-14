from .views import NationalityRequestDetailView,NationalityCreateView,NationalitiesBatchDetailView
from django.urls import path,include


urlpatterns = [
    path('nationalities/', NationalityCreateView.as_view(), name='nationality-list-create'),
    path('nationalities/<uuid:pk>/', NationalityRequestDetailView.as_view(), name='nationality-detail'),
    path('nationalities/batch/', NationalitiesBatchDetailView.as_view(), name='nationality-batch-detail'),]
