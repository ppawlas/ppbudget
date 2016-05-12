from rest_framework import permissions, viewsets
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.permissions import IsCategoryOwner, IsCategoriesOwner
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return permissions.AllowAny(),
        elif self.request.method in ('GET', 'HEAD'):
            return permissions.IsAuthenticated(), permissions.IsAdminUser(),
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return permissions.IsAuthenticated(), IsCategoryOwner(),
        else:   # self.request.method == 'POST'
            return permissions.IsAuthenticated(),

    def perform_create(self, serializer: CategorySerializer):

        serializer.save(user=self.request.user)

        return super(CategoryViewSet, self).perform_create(serializer)


class UserCategoriesViewSet(viewsets.ViewSet):
    queryset = Category.objects.select_related('user').all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated(), IsCategoriesOwner(),

    def list(self, request, user_username=None):
        queryset = self.queryset.filter(user__username=user_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
