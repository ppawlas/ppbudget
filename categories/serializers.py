from rest_framework import serializers
from authentication.serializers import UserSerializer
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id', 'user', 'parent', 'name', 'event_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
