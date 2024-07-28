from django.contrib import admin
from .models import Housekeeper,HireRequest,RecruitmentRequest,TransferRequest,Status



# Register your models here.

admin.site.register(Housekeeper)
admin.site.register(HireRequest)
admin.site.register(RecruitmentRequest)
admin.site.register(TransferRequest)
admin.site.register(Status)



