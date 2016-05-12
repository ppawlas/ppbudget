from rest_framework import permissions, viewsets
from tags.models import Tag
from tags.serializers import TagSerializer
from tags.permissions import IsTagOwner, IsTagsOwner
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by('name')
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return permissions.AllowAny(),
        elif self.request.method in ('GET', 'HEAD'):
            return permissions.IsAuthenticated(), permissions.IsAdminUser(),
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return permissions.IsAuthenticated(), IsTagOwner(),
        else:   # self.request.method == 'POST'
            return permissions.IsAuthenticated(),

    def perform_create(self, serializer: TagSerializer):
        serializer.save(user=self.request.user)

        return super(TagViewSet, self).perform_create(serializer)


class UserTagsViewSet(viewsets.ViewSet):
    queryset = Tag.objects.select_related('user').all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsTagsOwner(),

    def list(self, request, user_username=None):
        queryset = self.queryset.filter(user__username=user_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
