from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, "user"):
            owner = obj.user
        elif hasattr(obj, "author"): 
            owner = obj.author
        else:
            return False
        return owner == request.user or request.user.is_staff
    
class CustomQuestionPermission(permissions.BasePermission):
    """
    Custom permission to allow:
    - Anyone to read (GET, HEAD, OPTIONS)
    - Authenticated users to create (POST)
    - Owners to update (PUT, PATCH)
    - Admins to delete (DELETE)
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return obj.author == request.user or request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False