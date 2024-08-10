from django.urls import path
from .views import DiscountCreateView,DiscountRetrieveUpdateDestroyView,PromotionCodeCreateView,PromotionCodeRetrieveUpdateDestroyView


urlpatterns = [
    path('discounts/', DiscountCreateView.as_view(), name='discount-list-create'),
    path('discounts/<uuid:pk>/', DiscountRetrieveUpdateDestroyView.as_view(), name='discount-retrieve-update-destroy'),
    path('promotion-codes/', PromotionCodeCreateView.as_view(), name='promotion-code-list-create'),
    path('promotion-codes/<int:pk>/', PromotionCodeRetrieveUpdateDestroyView.as_view(), name='promotion-code-detail'),
]