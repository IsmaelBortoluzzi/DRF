from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        
    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id

