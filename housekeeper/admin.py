from django.contrib import admin
from .models import Housekeeper,HireRequest,RecruitmentRequest,TransferRequest



# Register your models here.

admin.site.register(Housekeeper)
admin.site.register(HireRequest)
admin.site.register(RecruitmentRequest)
admin.site.register(TransferRequest)



