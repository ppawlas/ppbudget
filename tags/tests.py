from django.contrib.auth.models import User
from tags.models import Tag
from tags.views import TagViewSet
from rest_framework import status
from rest_framework.test import APITestCase


class TagTestCase(APITestCase):
    def setUp(self):
        test_user_1 = User.objects.create(username='test_user_1', is_staff=True)
        test_user_2 = User.objects.create(username='test_user_2')
        Tag.objects.create(user=test_user_1, name='test_tag_1')
        Tag.objects.create(user=test_user_2, name='test_tag_2')
        Tag.objects.create(user=test_user_2, name='test_tag_3')

    def test_get_all_tags_no_auth(self):
        url = '/api/v1/tags/'

        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('results', response.data)

    def test_get_all_tags_as_user(self):
        user = User.objects.get(username='test_user_2')
        url = '/api/v1/tags/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('results', response.data)

    def test_get_all_tags_as_admin(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/tags/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 3)
        self.assertIn('results', response.data)
        self.assertEquals(response.data['results'][0]['user']['username'], 'test_user_1')
        self.assertEquals(response.data['results'][0]['name'], 'test_tag_1')

    def test_get_user_tags_no_auth(self):
        user_1 = User.objects.get(username='test_user_1')
        url = '/api/v1/users/' + user_1.username + '/tags/'

        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_tags_no_owner(self):
        user_1 = User.objects.get(username='test_user_1')
        user_2 = User.objects.get(username='test_user_2')
        url = '/api/v1/users/' + user_1.username + '/tags/'

        self.client.force_login(user_2)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_tags_as_owner(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/users/' + user.username + '/tags/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['user']['username'], 'test_user_1')
        self.assertEquals(response.data[0]['name'], 'test_tag_1')

    def test_post_tag_no_auth(self):
        url = '/api/v1/tags/'
        new_tag_name = 'test_tag_4'
        data = {'name': new_tag_name}

        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertFalse(TagViewSet.queryset.filter(name=new_tag_name).exists())

    def test_post_tag_auth(self):
        user = User.objects.get(username='test_user_2')
        new_tag_name = 'test_tag_4'
        url = '/api/v1/tags/'
        data = {'name': new_tag_name}

        self.client.force_login(user)
        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(response.data), 5)    # number of serializer fields
        self.assertEquals(response.data['user']['username'], user.username)
        self.assertEquals(response.data['name'], new_tag_name)
        # test model
        self.assertTrue(TagViewSet.queryset.filter(name=new_tag_name).exists())
        self.assertEquals(TagViewSet.queryset.get(name=new_tag_name).user.username, user.username)

    def test_patch_tag_no_auth(self):
        test_tag = Tag.objects.get(name='test_tag_3')
        new_tag_name = 'patched_test_tag_3'
        url = '/api/v1/tags/' + str(test_tag.id) + '/'
        data = {'name': new_tag_name}

        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertEquals(TagViewSet.queryset.get(id=test_tag.id).name, test_tag.name)

    def test_patch_tag_not_exist(self):
        user = User.objects.get(username='test_user_1')
        new_tag_name = 'patched_test_tag_3'
        url = '/api/v1/tags/999/'
        data = {'name': new_tag_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_tag_no_owner(self):
        user = User.objects.get(username='test_user_1')
        test_tag = Tag.objects.get(name='test_tag_3')
        new_tag_name = 'patched_test_tag_3'
        url = '/api/v1/tags/' + str(test_tag.id) + '/'
        data = {'name': new_tag_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertEquals(TagViewSet.queryset.get(id=test_tag.id).name, test_tag.name)

    def test_patch_tag_as_owner(self):
        user = User.objects.get(username='test_user_2')
        test_tag = Tag.objects.get(name='test_tag_3')
        new_tag_name = 'patched_test_tag_3'
        url = '/api/v1/tags/' + str(test_tag.id) + '/'
        data = {'name': new_tag_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)  # number of serializer fields
        self.assertEquals(response.data['id'], test_tag.id)
        self.assertEquals(response.data['name'], new_tag_name)
        # test model
        self.assertEquals(TagViewSet.queryset.get(id=test_tag.id).name, new_tag_name)

    def test_delete_tag_no_auth(self):
        test_tag = Tag.objects.get(name='test_tag_2')
        url = '/api/v1/tags/' + str(test_tag.id) + '/'

        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertTrue(TagViewSet.queryset.filter(id=test_tag.id).exists())

    def test_delete_tag_not_exist(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/tags/999/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_tag_no_owner(self):
        user = User.objects.get(username='test_user_1')
        test_tag = Tag.objects.get(name='test_tag_2')
        url = '/api/v1/tags/' + str(test_tag.id) + '/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertTrue(TagViewSet.queryset.filter(id=test_tag.id).exists())

    def test_delete_tag_as_owner(self):
        user = User.objects.get(username='test_user_2')
        test_tag = Tag.objects.get(name='test_tag_2')
        url = '/api/v1/tags/' + str(test_tag.id) + '/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        # test model
        self.assertFalse(TagViewSet.queryset.filter(id=test_tag.id).exists())
