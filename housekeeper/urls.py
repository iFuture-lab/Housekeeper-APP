# urls.py

from django.urls import path
from .views import (
    HousekeeperListCreateView, HousekeeperDetailView,
    HireRequestListCreateView, HireRequestDetailView,
    RecruitmentRequestListCreateView, RecruitmentRequestDetailView,
    TransferRequestListCreateView, TransferRequestDetailView
)

urlpatterns = [
    path('housekeepers/', HousekeeperListCreateView.as_view(), name='housekeeper-list-create'),
    path('housekeepers/<int:pk>/', HousekeeperDetailView.as_view(), name='housekeeper-detail'),

    path('hire-requests/', HireRequestListCreateView.as_view(), name='hire-request-list-create'),
    path('hire-requests/<int:pk>/', HireRequestDetailView.as_view(), name='hire-request-detail'),

    path('recruitment-requests/', RecruitmentRequestListCreateView.as_view(), name='recruitment-request-list-create'),
    path('recruitment-requests/<int:pk>/', RecruitmentRequestDetailView.as_view(), name='recruitment-request-detail'),

    path('transfer-requests/', TransferRequestListCreateView.as_view(), name='transfer-request-list-create'),
    path('transfer-requests/<int:pk>/', TransferRequestDetailView.as_view(), name='transfer-request-detail'),
]
