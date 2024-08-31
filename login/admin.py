from django.contrib import admin
from .models import CustomUser ,OtpMessage,OTPLog
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


#################################### register the models in database ###########################################

# class CustomUserAdmin(UserAdmin):
    
#     fieldsets = (
#         *UserAdmin.fieldsets,
#                  ('Additional Info',{
#                      'fields':('role'
#                                )
#                  }
#                   )
                 
#                  )
                 
   

    


admin.site.register(CustomUser)
admin.site.register(OtpMessage)
admin.site.register(OTPLog)
# admin.site.register(AdminUser,CustomUserAdmin)