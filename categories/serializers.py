from rest_framework import serializers
from authentication.serializers import UserSerializer
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False, default=serializers.CurrentUserDefault())
    children = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if not kwargs.pop('with_children', False):
            self.fields.pop('children')

        super(CategorySerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        if 'parent' in data and data['parent'] and data['parent'].user != data['user']:
            raise serializers.ValidationError('Parent category user does not match.')

        if 'parent' in data and data['parent'] and data['parent'].event_type != data['event_type']:
            raise serializers.ValidationError('Parent category event type does not match.')

        if self.instance and 'parent' in data and data['parent'] and \
                self.__is_circular_reference__(self.instance.id, data['parent']):
            raise serializers.ValidationError('Circular references are prohibited.')

        return super(CategorySerializer, self).validate(data)

    def get_children(self, obj):
        children = self.instance.filter(parent=obj.id)
        if children.exists():
            return [child.id for child in children.all()]
        else:
            return []

    def __is_circular_reference__(self, category_id, new_parent):
        if not new_parent.parent:
            return False
        elif new_parent.id == category_id or new_parent.parent.id == category_id:
            return True
        else:
            return self.__is_circular_reference__(category_id, new_parent.parent)

    class Meta:
        model = Category
        fields = ('id', 'user', 'parent', 'name', 'event_type', 'root_node', 'children', 'created_at', 'updated_at')
        read_only_fields = ('id', 'root_node', 'children', 'created_at', 'updated_at')
