from rest_framework import permissions
from categories.models import Category


class IsCategoryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, category: Category):
        if request.user:
            return category.user == request.user
        return False
