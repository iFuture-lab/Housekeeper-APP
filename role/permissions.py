from rest_framework import permissions

class HasPermission(permissions.BasePermission):
    """
    Custom permission to check if the user has the required permission.
    """

    def has_permission(self, request, view):
        # Get the required permission from the view
        required_permission = getattr(view, 'permission_required', None)
        user = request.user
        
        # Superusers bypass permission checks
        if user.is_superuser:
            return True
        
        # Ensure the user is authenticated
        if not user.is_authenticated:
            return False
        
        # Check if the user has the required permission
        user_roles = user.roles.all()  # Assuming 'roles' is a related name for user's roles
        for role in user_roles:
            if role.permissions.filter(name=required_permission).exists():
                return True
                
        return False
