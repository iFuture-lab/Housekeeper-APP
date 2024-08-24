from .views import NationalityRequestDetailView,NationalityCreateView,NationalitiesBatchDetailView
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('nationalities/', NationalityCreateView.as_view(), name='nationality-list-create'),
    path('nationalities/<uuid:pk>/', NationalityRequestDetailView.as_view(), name='nationality-detail'),
    path('nationalities/batch/', NationalitiesBatchDetailView.as_view(), name='nationality-batch-detail'),]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)