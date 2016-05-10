from rest_framework import serializers
from authentication.serializers import UserSerializer
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ('id', 'user', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
