from rest_framework import permissions, viewsets
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.permissions import IsCategoryOwner, IsCategoriesOwner
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('user', '-root_node', 'event_type', 'name')
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
        queryset = self.queryset.filter(user__username=user_username).order_by('-root_node', 'event_type', 'name')
        serializer = self.serializer_class(queryset, many=True, with_children=True)

        lookup = {category['id']: category for category in serializer.data}
        tree = [self.__fill_children__(category, lookup) for category in serializer.data if category['root_node']]

        return Response(tree)

    def __fill_children__(self, category, lookup):
        if len(category['children']) > 0:
            category['children'] = [self.__fill_children__(lookup[child_id], lookup)
                                    for child_id in category['children']]

        return category
