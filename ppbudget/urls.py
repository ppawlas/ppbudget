"""ppbudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_nested import routers
from ppbudget.views import IndexView
from authentication.views import UserViewSet, GroupViewSet
from categories.views import CategoryViewSet, UserCategoriesViewSet
from tags.views import TagViewSet, UserTagsViewSet
from events.views import ResourceViewSet, EventViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'events', EventViewSet)

tags_router = routers.NestedSimpleRouter(
    router, r'users', lookup='user'
)
tags_router.register(r'tags', UserTagsViewSet)

categories_router = routers.NestedSimpleRouter(
    router, r'users', lookup='user'
)
categories_router.register(r'categories', UserCategoriesViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(tags_router.urls)),
    url(r'^api/v1/', include(categories_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url('^.*$', IndexView.as_view(), name='index'),
]
