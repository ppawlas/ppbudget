from rest_framework import permissions, viewsets
from events.models import Resource, Event, Operation
from events.serializers import ResourceSerializer, EventSerializer, OperationSerializer
from events.permissions import IsResourceOwner, IsEventOwner, IsOperationOwner


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.order_by('name')
    serializer_class = ResourceSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(), IsResourceOwner()

    def perform_create(self, serializer: ResourceSerializer):
        serializer.save(user=self.request.user)

        return super(ResourceViewSet, self).perform_create(serializer)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.order_by('-event_date')
    serializer_class = EventSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(), IsEventOwner()

    def perform_create(self, serializer: EventSerializer):
        serializer.save(user=self.request.user)

        return super(EventViewSet, self).perform_create(serializer)
