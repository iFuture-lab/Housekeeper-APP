from django.urls import path
from .views import UserInterestByCustomer, ContractCreateView, ContractListView, ContractDetailView,UserInterestCreateView, UserInterestListView, UserInterestReportView,ContractsByRequester, ContractBatchView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<uuid:pk>/', ContractDetailView.as_view(), name='contract-detail'),
    path('contracts/batch/', ContractBatchView.as_view(), name='contract-batch'),
    path('contracts/customer/', ContractsByRequester.as_view(), name='contract-detail'),
    path('users-interests/', UserInterestListView.as_view(), name='user-interest-list'),
    path('users-interests/customer/', UserInterestByCustomer.as_view(), name='user-interest-detail'),
    path('users-interests/create/', UserInterestCreateView.as_view(), name='user-interest-create'),
    path('users-interests/report/', UserInterestReportView.as_view(), name='user-interest-report'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)