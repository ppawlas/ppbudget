from django.test import TestCase
from django.contrib.auth.models import User
from tags.models import Tag
from tags.views import TagViewSet
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class TagTestCase(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create(username='test_user_1')
        test_user_2 = User.objects.create(username='test_user_2')
        Tag.objects.create(user=test_user_1, name='test_tag_1')
        Tag.objects.create(user=test_user_2, name='test_tag_2')

    def test_get_tags_no_auth(self):
        factory = APIRequestFactory()
        view = TagViewSet.as_view({'get': 'list'})

        request = factory.get('/api/v1/tags/')
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('results', response.data)

    def test_get_tags(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='test_user_1')
        view = TagViewSet.as_view({'get': 'list'})

        request = factory.get('/api/v1/tags/')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 2)
        self.assertIn('results', response.data)
        self.assertEquals(response.data['results'][0]['user']['username'], 'test_user_1')
        self.assertEquals(response.data['results'][0]['name'], 'test_tag_1')
