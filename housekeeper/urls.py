# urls.py

from django.urls import path
from .views import HousekeeperRequestCreateView, HousekeeperRequestListView, HousekeeperRequestUpdateView, HousekeeperRequestDeleteView

urlpatterns = [
    # Other URL patterns...
    path('requests/new/', HousekeeperRequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/update/', HousekeeperRequestUpdateView.as_view(), name='request-update'),
    path('requests/<int:pk>/delete/', HousekeeperRequestDeleteView.as_view(), name='request-delete'),
]
