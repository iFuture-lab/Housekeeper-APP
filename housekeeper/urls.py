# urls.py

from django.urls import path

urlpatterns = [
    # Other URL patterns...
    
    path('requests/<int:pk>/update/', HousekeeperRequestUpdateView.as_view(), name='request-update'),
    
]
