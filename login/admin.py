from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




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
# admin.site.register(AdminUser,CustomUserAdmin)