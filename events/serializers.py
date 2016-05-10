from rest_framework import serializers
from authentication.serializers import UserSerializer
from tags.serializers import TagSerializer
from events.models import Resource, Event, Operation


class ResourceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Resource
        fields = ('id', 'user', 'name', 'initial_balance', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class OperationSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)

    class Meta:
        model = Operation
        fields = ('id', 'resource', 'flow', 'created_at', 'updated_at')
        read_only_fields = ('id', 'resource', 'created_at', 'updated_at')


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True)
    operations = OperationSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'description', 'event_type', 'event_date', 'category', 'tags', 'operations',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        operations_data = validated_data.pop('operations')
        tags_data = validated_data.pop('tags')

        event = Event.objects.create(**validated_data)

        for tag_data in tags_data:
            event.tags.add(tag_data)

        for operation_data in operations_data:
            Operation.objects.create(event=event, **operation_data)

        return event
