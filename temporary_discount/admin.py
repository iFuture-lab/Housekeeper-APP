from django.contrib import admin
from .models import TempoararyDiscount,PromotionCode,CustomPackage,CustomPackageNationallity
# Register your models here.

admin.site.register(TempoararyDiscount)
admin.site.register(PromotionCode)
admin.site.register(CustomPackage)
admin.site.register(CustomPackageNationallity)

