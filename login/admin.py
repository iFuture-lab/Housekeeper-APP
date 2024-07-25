from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # Make sure to import your custom user model

#  #Define custom forms
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = RoleUser
#         fields = ('role',)

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = RoleUser
#         fields = ('role',)
        
        
# # Define custom admin
# class CustomUserAdmin(UserAdmin):
#     model = RoleUser
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
    
#     list_display = ['role']
    
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('role',)}),
#     )
    
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('role',)}),
#     )
    
#     filter_horizontal = UserAdmin.filter_horizontal


# # Register your models here.

admin.site.register(CustomUser)
# admin.site.register(User)