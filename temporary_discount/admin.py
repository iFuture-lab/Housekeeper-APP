from django.contrib import admin
from .models import TempoararyDiscount,PromotionCode
# Register your models here.

admin.site.register(TempoararyDiscount)
admin.site.register(PromotionCode)

