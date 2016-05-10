from rest_framework import permissions
from tags.models import Tag


class IsTagOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, tag: Tag):
        if request.user:
            return tag.user == request.user
        return False
