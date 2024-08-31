from django.urls import path
from .views import ContractCreateView, ContractListView, ContractDetailView,UserInterestCreateView, UserInterestListView, UserInterestReportView

urlpatterns = [
    path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/create/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<uuid:pk>/', ContractDetailView.as_view(), name='contract-detail'),
    #  path('users-interests/', UserInterestListView.as_view(), name='user-interest-list'),
    # path('users-interests/create/', UserInterestCreateView.as_view(), name='user-interest-create'),
    # path('users-interests/report/', UserInterestReportView.as_view(), name='user-interest-report'),
    
]
