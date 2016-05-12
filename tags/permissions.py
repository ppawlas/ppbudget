from rest_framework import permissions
from tags.models import Tag


class IsTagOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, tag: Tag):
        if request.user:
            return tag.user == request.user
        return False


class IsTagsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and view.kwargs['user_username']:
            return request.user.username == view.kwargs['user_username']
        return False
