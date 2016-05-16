from rest_framework import serializers
from authentication.serializers import UserSerializer
from tags.serializers import TagSerializer
from events.models import Resource, Event, Operation


class ResourceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Resource
        fields = ('id', 'user', 'name', 'initial_balance', 'current_balance', 'created_at', 'updated_at')
        read_only_fields = ('id', 'current_balance', 'created_at', 'updated_at')


class OperationSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)

    class Meta:
        model = Operation
        fields = ('id', 'resource', 'event', 'flow', 'created_at', 'updated_at')
        read_only_fields = ('id', 'resource', 'event', 'created_at', 'updated_at')


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True)
    operations = OperationSerializer(many=True)

    def validate(self, data):
        if data['category'].event_type != data['event_type']:
            raise serializers.ValidationError('Event type and category type do not match.')
        if data['category'].user != data['user']:
            raise serializers.ValidationError('Event user and category user do not match.')
        if 'tags' in data and data['tags'] and len([tag for tag in data['tags'] if tag.user != data['user']]) > 0:
            raise serializers.ValidationError('Event user and at least one tag user do not match.')
        if 'operations' in data and data['operations'] and \
                len([operation for operation in data['operations'] if operation.resource.user != data['user']]) > 0:
            raise serializers.ValidationError('Event user and at least one operation resource user do not match.')

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

    # TODO update method
