from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit it.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin and owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


def permision_or(permision1, permision2):
    class Permision(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            return permision1.has_object_permission(self=self, request=request, view=view, obj=obj) or \
                   permision2.has_object_permission(self=self, request=request, view=view, obj=obj)

        def has_permission(self, request, view):
            return permision1.has_permision(self=self, request=request, view=view) or \
                   permision2.has_permision(self=self, request=request, view=view)

    return Permision
