from rest_framework import permissions
from events.models import Resource, Event, Operation


class IsResourceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, resource):
        if request.user:
            return resource.user == request.user
        return False


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        if request.user:
            return event.user == request.user
        return False


class IsOperationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, operation: Operation):
        if request.user:
            resource = Resource.objects.get(id=operation.resource.id)
            event = Event.objects.get(id=operation.event.id)
            return (resource.user == request.user) and (event.user == request.user)
        return False
