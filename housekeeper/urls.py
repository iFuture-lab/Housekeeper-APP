# urls.py

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    HousekeeperListCreateView, HousekeeperDetailView,
    HireRequestListCreateView, HireRequestDetailView,
    RecruitmentRequestListCreateView, RecruitmentRequestDetailView,
    TransferRequestListCreateView, TransferRequestDetailView
   
)
from .views import HousekeeperIDsView,AvailableHousekeeper,TransferBatchStatusUpdateView,RecruitmentBatchStatusUpdateView,HireRequestListView,TransferRequestListView
from.views import HousekeeperBatchDetailView,HireHousekeeperBatchDetailView,RecruitmentRequestBatchDetailView,TransferRequestBatchDetailView,HousekeeperBatchStatusUpdateView,RecruitmentListView
from .status_view import StatusCreateView,StatusDetailView,StatusBatchDetailView
from .religion_view import ReligionCreateView, ReligionBatchDetailView,ReligionDetailView
from .employment_type_view import EmploymentTypeCreateView, EmploymentTypeBatchDetailView,EmploymentTypeDetailView
# from .views import ActionLogViewSet



# router = DefaultRouter()
# router.register(r'action-logs', ActionLogViewSet)

urlpatterns = [
    path('housekeepers/', HousekeeperListCreateView.as_view(), name='housekeeper-list-create'),
    path('housekeepers/<uuid:pk>/', HousekeeperDetailView.as_view(), name='housekeeper-detail'),
    path('housekeeper/ids/', HousekeeperIDsView.as_view(), name='housekeeper-ids'),
    path('housekeepers/batch/', HousekeeperBatchDetailView.as_view(), name='housekeeper-batch-detail'),
    #path('housekeepers/DeleteMany/', HousekeeperBatchDeleteView.as_view(), name='housekeeper-delete-detail'),
    path('housekeepers/search/', AvailableHousekeeper.as_view(), name='available-housekeeper-list'),
    
    
    path('hire-requests/', HireRequestListCreateView.as_view(), name='hire-request-list-create'),
    path('hire-requests/<uuid:pk>/', HireRequestDetailView.as_view(), name='hire-request-detail'),
    path('hire-requests/batch/', HireHousekeeperBatchDetailView.as_view(), name='hire-request-batch-detail'),
    #path('hire-requests/batch/', HireHousekeeperBatchDetailView.as_view(), name='hire-request-batch-detail'),
    path('hire-requests/batch/status', HousekeeperBatchStatusUpdateView.as_view(), name='hire-request-batch-status'),
    path('hire-requests/status/filter', HireRequestListView.as_view(), name='hire-request-batch-status-filter'),
    

    path('recruitment-requests/', RecruitmentRequestListCreateView.as_view(), name='recruitment-request-list-create'),
    path('recruitment-requests/<uuid:pk>/', RecruitmentRequestDetailView.as_view(), name='recruitment-request-detail'),
    path('recruitment-requests/batch/', RecruitmentRequestBatchDetailView.as_view(), name='recruitment-request-batch-detail'),
    path('recruitment-requests/batch/status', RecruitmentBatchStatusUpdateView.as_view(), name='recruitment-request-batch-detail'), 
    path('recruitment-requests/status/filter',RecruitmentListView.as_view(), name='recruitment-request-batch-status-filter'),   

    path('transfer-requests/', TransferRequestListCreateView.as_view(), name='transfer-request-list-create'),
    path('transfer-requests/<uuid:pk>/', TransferRequestDetailView.as_view(), name='transfer-request-detail'),
    path('transfer-requests/batch/', TransferRequestBatchDetailView.as_view(), name='transfer-request-batch-detail'),
    path('transfer-requests/batch/status', TransferBatchStatusUpdateView.as_view(), name='transfer-request-batch-detail'), 
    path('transfer-requests/status/filter',TransferRequestListView.as_view(), name='transfer-request-batch-status-filter'),
    
    
    path('status/',StatusCreateView.as_view(), name='status-create'),
    path('status/<uuid:pk>/',StatusDetailView.as_view(), name='status-detail'),
    path('status/batch/',StatusBatchDetailView.as_view(), name='status-batch'),
    
    path('religion/',ReligionCreateView.as_view(), name='religion-create'),
    path('religion/<uuid:pk>/',ReligionDetailView.as_view(), name='religion-detail'),
    path('religion/batch/',ReligionBatchDetailView.as_view(), name='religion-batch'),
    
    path('employement-type/',EmploymentTypeCreateView.as_view(), name='employement-type-create'),
    path('employement-type/<uuid:pk>/',EmploymentTypeDetailView.as_view(), name='employement-type-detail'),
    path('employement-type/batch/',EmploymentTypeBatchDetailView.as_view(), name='employement-type-batch'),
    # path('action-log', include(router.urls)),
    
    
    
    
    
    
   
]
