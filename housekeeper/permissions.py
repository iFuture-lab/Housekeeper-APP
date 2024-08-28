from rest_framework.permissions import BasePermission
from role_per_user.models import RolePerClient,RolePerUser

from django.contrib.auth.models import User
from login.models import CustomUser
from rest_framework import permissions
from django.contrib.auth import get_user_model

class RolePermission(BasePermission):
    """
    Custom permission class that checks if the user has the required permissions
    for various CRUD operations.
    """
    
    
    def has_permission(self, request, view):
        required_permissions = getattr(view, 'required_permissions', None)

        if not required_permissions:
            print("hiiiiiiiiiiiiiiii")
            return True 

        method_permissions = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        
        operation = method_permissions.get(request.method)
        if not operation:
            print("Operation not recognized.")
            return False  # Disallow access if the operation type is not recognized

        try:
            if isinstance(request.user, User):
                print("i found the user")
                return self.user_has_permission(request.user, operation)
            elif isinstance(request.user, CustomUser):
                print("i found the client")
                return self.client_has_permission(request.user, operation)
            
            else:
                print("Unknown user instance type.")
                return False
        except Exception as e:
            print("Error in permission check.")
            print(f"Error details: {e}")
            return False
        

    
    

    def user_has_permission(self, user, permission_name):
         # Ensure the user is of type User
        if not isinstance(user, User):
            print("Expected User instance but found different type.")
            return False
        
        role_per_users = RolePerUser.objects.filter(users=user)
        print(f"User roles: {role_per_users}")

        for role_per_user in role_per_users:
            role = role_per_user.role
            print(f"Checking role: {role}")
            if role.permissions.filter(name=permission_name).exists():
                print(f"Permission '{permission_name}' found for role.")
                return True

        print(f"Permission '{permission_name}' not found for any roles.")
        return False
    
    
    
    def client_has_permission(self, user, permission_name):
      
        role_per_clients = RolePerClient.objects.filter(clients=user)
        print(f"User roles: {role_per_clients}")
        
        for role_per_client in role_per_clients:
            role = role_per_client.role
            print(f"Checking role: {role}")
            if role.permissions.filter(name=permission_name).exists():
                print("i gottttttttttttt the permission")
                print(f"Permission '{permission_name}' found for role.")
                return True
               
        print(f"Permission '{permission_name}' not found for any roles.")
        return False
    


class MethodBasedPermissionsMixin:
    
    permission_classes = [RolePermission]  

    def get_permissions(self):
      
        if self.request.method == 'GET':
            self.required_permissions = ['read']
        elif self.request.method == 'POST':
            self.required_permissions = ['create']
        elif self.request.method in ['PUT', 'PATCH']:
            self.required_permissions = ['update']
        elif self.request.method == 'DELETE':
            self.required_permissions = ['delete']
        else:
            self.required_permissions = []

        return super().get_permissions()
    
    
    
    
    
    

    
    
    
    
    
    
    
  
