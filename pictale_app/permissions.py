from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors or admins to edit/delete an object.
    Everyone else can read (GET requests) only.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are allowed only to the author or admin
        return obj.author == request.user or request.user.is_staff
