from rest_framework import permissions, viewsets
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.permissions import IsCategoryOwner


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(), IsCategoryOwner()

    def perform_create(self, serializer: CategorySerializer):
        serializer.save(user=self.request.user)

        return super(CategoryViewSet, self).perform_create(serializer)
