from django.urls import path
from .views import ContractCreateView, ContractListView, ContractDetailView

urlpatterns = [
    path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/create/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<uuid:pk>/', ContractDetailView.as_view(), name='contract-detail'),
]
