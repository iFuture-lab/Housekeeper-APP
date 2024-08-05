from django.urls import path
from .views import payment_callback

urlpatterns = [
    # other URL patterns
    path('edfapay/callback/', payment_callback, name='edfapay_callback'),
]
