from rest_framework import permissions, viewsets
from tags.models import Tag
from tags.serializers import TagSerializer
from tags.permissions import IsTagOwner
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by('name')
    serializer_class = TagSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(), permissions.IsAdminUser()

    def perform_create(self, serializer: TagSerializer):
        serializer.save(user=self.request.user)

        return super(TagViewSet, self).perform_create(serializer)


class UserTagsViewSet(viewsets.ViewSet):
    queryset = Tag.objects.select_related('user').all()
    serializer_class = TagSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(user__username=account_username)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)