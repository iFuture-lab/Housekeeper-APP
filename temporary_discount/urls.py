from django.urls import path
from .views import DiscountCreateView,DiscountRetrieveUpdateDestroyView,PromotionCodeCreateView,PromotionCodeRetrieveUpdateDestroyView,PackageByRequestTypeView,PackageCreateView,PackageRetrieveUpdateDestroyView


urlpatterns = [
    path('discounts/', DiscountCreateView.as_view(), name='discount-list-create'),
    path('discounts/<uuid:pk>/', DiscountRetrieveUpdateDestroyView.as_view(), name='discount-retrieve-update-destroy'),
    path('custom-packages/', PackageCreateView.as_view(), name='custom-package'),
    path('custom-packages/<uuid:pk>/', PackageRetrieveUpdateDestroyView.as_view(), name='custom-package-detail'),
    path('custom-packages-by-request-type/<uuid:request_type_id>/', PackageByRequestTypeView.as_view(), name='packages-by-request-type'),
    path('promotion-codes/', PromotionCodeCreateView.as_view(), name='promotion-code-list-create'),
    path('promotion-codes/<uuid:pk>/', PromotionCodeRetrieveUpdateDestroyView.as_view(), name='promotion-code-detail'),
   # path('custom-package/request-type/<uuid:request_type_id>', PackageByRequestTypeView.as_view(), name='packages-by-request-type'),
    # path('custom-package/request-type/<uuid:request_type_id>/', PackageByRequestTypeView.as_view(), name='packages-by-request-type'),

]