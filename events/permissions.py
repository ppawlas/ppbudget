from rest_framework import permissions
from events.models import Resource, Event, Operation


class IsResourceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, resource):
        if request.user:
            return resource.user == request.user
        return False


class IsResourcesOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and view.kwargs['user_username']:
            return request.user.username == view.kwargs['user_username']
        return False


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        if request.user:
            return event.user == request.user
        return False


class IsEventsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and view.kwargs['user_username']:
            return request.user.username == view.kwargs['user_username']
        return False


class IsOperationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, operation: Operation):
        if request.user:
            resource = Resource.objects.get(id=operation.resource.id)
            event = Event.objects.get(id=operation.event.id)
            return (resource.user == request.user) and (event.user == request.user)
        return False


class IsOperationsResourceOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            resource = Resource.objects.get(id=view.kwargs['resource_pk'])
            return request.user.username == resource.user.username
        return False


class IsOperationsEventOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            event = Event.objects.get(id=view.kwargs['event_pk'])
            return request.user.username == event.user.username
        return False
