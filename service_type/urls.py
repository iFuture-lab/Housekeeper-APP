from .views import ServiceByRequestStatus, ServiceCreateView,ServiceDetailView,ServiceBatchDetailView, ServiceByRequest
from django.urls import path,include

urlpatterns = [
    path('services/', ServiceCreateView.as_view(), name='service-list-create'),
    path('services/requests/', ServiceByRequest.as_view(), name='service-by-request'),
    path('services/requests-status/', ServiceByRequestStatus.as_view(), name='service-by-request-status'),
    path('services/<uuid:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/batch/', ServiceBatchDetailView.as_view(), name='service-batch-detail'),]


