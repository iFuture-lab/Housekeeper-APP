from django.contrib import admin
from .models import ActionLog
from .models import Housekeeper,HireRequest,RecruitmentRequest,TransferRequest,Status,Religion,EmploymentType



# Register your models here.

admin.site.register(Housekeeper)
admin.site.register(HireRequest)
admin.site.register(RecruitmentRequest)
admin.site.register(TransferRequest)
admin.site.register(Status)
admin.site.register(Religion)
admin.site.register(EmploymentType)


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'description', 'timestamp')



