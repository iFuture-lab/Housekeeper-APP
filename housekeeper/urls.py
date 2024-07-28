# urls.py

from django.urls import path
from .views import (
    HousekeeperListCreateView, HousekeeperDetailView,
    HireRequestListCreateView, HireRequestDetailView,
    RecruitmentRequestListCreateView, RecruitmentRequestDetailView,
    TransferRequestListCreateView, TransferRequestDetailView
   
)
from .views import HousekeeperIDsView, HousekeeperBatchDeleteView,AvailableHousekeeper,TransferBatchStatusUpdateView,RecruitmentBatchStatusUpdateView
from.views import HousekeeperBatchDetailView,HireHousekeeperBatchDetailView,RecruitmentRequestBatchDetailView,TransferRequestBatchDetailView,HousekeeperBatchStatusUpdateView
urlpatterns = [
    path('housekeepers/', HousekeeperListCreateView.as_view(), name='housekeeper-list-create'),
    path('housekeepers/<int:pk>/', HousekeeperDetailView.as_view(), name='housekeeper-detail'),
    path('housekeeper/ids/', HousekeeperIDsView.as_view(), name='housekeeper-ids'),
    path('housekeepers/batch/', HousekeeperBatchDetailView.as_view(), name='housekeeper-batch-detail'),
    #path('housekeepers/DeleteMany/', HousekeeperBatchDeleteView.as_view(), name='housekeeper-delete-detail'),
    path('housekeepers/available/', AvailableHousekeeper.as_view(), name='available-housekeeper-list'),
    
    
    path('hire-requests/', HireRequestListCreateView.as_view(), name='hire-request-list-create'),
    path('hire-requests/<int:pk>/', HireRequestDetailView.as_view(), name='hire-request-detail'),
    path('hire-requests/batch/', HireHousekeeperBatchDetailView.as_view(), name='hire-request-batch-detail'),
    #path('hire-requests/batch/', HireHousekeeperBatchDetailView.as_view(), name='hire-request-batch-detail'),
    path('hire-requests/batch/status', HousekeeperBatchStatusUpdateView.as_view(), name='hire-request-batch-status'),

    path('recruitment-requests/', RecruitmentRequestListCreateView.as_view(), name='recruitment-request-list-create'),
    path('recruitment-requests/<int:pk>/', RecruitmentRequestDetailView.as_view(), name='recruitment-request-detail'),
    path('recruitment-requests/batch/', RecruitmentRequestBatchDetailView.as_view(), name='recruitment-request-batch-detail'),
    path('recruitment-requests/batch/status', RecruitmentBatchStatusUpdateView.as_view(), name='recruitment-request-batch-detail'),    

    path('transfer-requests/', TransferRequestListCreateView.as_view(), name='transfer-request-list-create'),
    path('transfer-requests/<int:pk>/', TransferRequestDetailView.as_view(), name='transfer-request-detail'),
    path('transfer-requests/batch/', TransferRequestBatchDetailView.as_view(), name='transfer-request-batch-detail'),
    path('transfer-requests/batch/status', TransferBatchStatusUpdateView.as_view(), name='transfer-request-batch-detail'),    
]
