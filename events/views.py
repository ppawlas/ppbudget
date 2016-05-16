from rest_framework import permissions, viewsets
from events.models import Resource, Event, Operation
from events.serializers import ResourceSerializer, EventSerializer, OperationSerializer
from events.permissions import IsResourceOwner, IsResourcesOwner, IsEventOwner, IsEventsOwner, \
    IsOperationOwner, IsOperationsResourceOwner, IsOperationsEventOwner
from rest_framework.response import Response


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.order_by('user', 'name')
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return permissions.AllowAny(),
        elif self.request.method in ('GET', 'HEAD'):
            return permissions.IsAuthenticated(), permissions.IsAdminUser(),
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return permissions.IsAuthenticated(), IsResourceOwner(),
        else:  # self.request.method == 'POST'
            return permissions.IsAuthenticated(),

    def perform_create(self, serializer: ResourceSerializer):
        serializer.save(user=self.request.user)

        return super(ResourceViewSet, self).perform_create(serializer)


class UserResourcesViewSet(viewsets.ViewSet):
    queryset = Resource.objects.select_related('user').all()
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsResourcesOwner(),

    def list(self, request, user_username=None):
        queryset = self.queryset.filter(user__username=user_username).order_by('name')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ResourceOperationsViewSet(viewsets.ViewSet):
    queryset = Operation.objects.select_related('resource').all()
    serializer_class = OperationSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsOperationsResourceOwner(),

    def list(self, request, resource_pk=None):
        queryset = self.queryset.filter(resource__id=resource_pk).order_by('-event__event_date')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.order_by('user', '-event_date', 'description')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return permissions.AllowAny(),
        elif self.request.method in ('GET', 'HEAD'):
            return permissions.IsAuthenticated(), permissions.IsAdminUser(),
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return permissions.IsAuthenticated(), IsEventOwner(),
        else:  # self.request.method == 'POST'
            return permissions.IsAuthenticated(),

    def perform_create(self, serializer: EventSerializer):
        serializer.save(user=self.request.user)

        return super(EventViewSet, self).perform_create(serializer)


class UserEventsViewSet(viewsets.ViewSet):
    queryset = Event.objects.select_related('user').all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsEventsOwner(),

    def list(self, request, user_username=None):
        queryset = self.queryset.filter(user__username=user_username).order_by('-event_date', 'description')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class EventOperationsViewSet(viewsets.ViewSet):
    queryset = Operation.objects.select_related('event').all()
    serializer_class = OperationSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsOperationsEventOwner(),

    def list(self, request, event_pk=None):
        queryset = self.queryset.filter(event__id=event_pk).order_by('resource__name')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

# TODO EventTagsViewSet
# TODO OperationViewSet
