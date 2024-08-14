from django.contrib import admin

from .models import RolePerUser,RolePerClient

# Register your models here.

admin.site.register(RolePerUser)
admin.site.register(RolePerClient)



