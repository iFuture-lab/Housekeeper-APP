from .views import ServiceCreateView,ServiceDetailView,ServiceBatchDetailView
from django.urls import path,include

urlpatterns = [
    path('services/', ServiceCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/batch/', ServiceBatchDetailView.as_view(), name='service-batch-detail'),]


