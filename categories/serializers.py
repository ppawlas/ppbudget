from rest_framework import serializers
from authentication.serializers import UserSerializer
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['parent'] and data['parent'].user != data['user']:
            raise serializers.ValidationError('Parent category user does not match.')

        if data['parent'] and data['parent'].event_type != data['event_type']:
            raise serializers.ValidationError('Parent category event type does not match.')

        return super(CategorySerializer, self).validate(data)

    class Meta:
        model = Category
        fields = ('id', 'user', 'parent', 'name', 'event_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
