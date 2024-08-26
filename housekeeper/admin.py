from django.contrib import admin
from .models import ActionLog
from .models import Housekeeper,HireRequest,RecruitmentRequest,TransferRequest,Status,Religion,EmploymentType,HousekeeperRequestType,Taxes



# Register your models here.

admin.site.register(Housekeeper)
admin.site.register(HireRequest)
admin.site.register(RecruitmentRequest)
admin.site.register(TransferRequest)
admin.site.register(Status)
admin.site.register(Religion)
admin.site.register(EmploymentType)
admin.site.register(HousekeeperRequestType)
admin.site.register(Taxes)


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'description', 'timestamp')
    
    

class HireRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('service_type',)



