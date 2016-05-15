from django.contrib.auth.models import User
from dictionaries.models import EventType
from categories.models import Category
from categories.views import CategoryViewSet
from rest_framework import status
from rest_framework.test import APITestCase


class TagTestCase(APITestCase):
    def setUp(self):
        test_user_1 = User.objects.create(username='test_user_1', is_staff=True)
        test_user_2 = User.objects.create(username='test_user_2')
        test_parent_category_1 = Category.objects.create(user=test_user_1, name='test_parent_category_1',
                                                         event_type=EventType.EXPENSE)
        Category.objects.create(user=test_user_1, parent=test_parent_category_1, name='test_child_category_1',
                                event_type=EventType.EXPENSE)
        Category.objects.create(user=test_user_2, name='test_parent_category_2',
                                event_type=EventType.INCOME)
        test_parent_category_3 = Category.objects.create(user=test_user_2, name='test_parent_category_3',
                                                         event_type=EventType.CHANGE)
        Category.objects.create(user=test_user_2, parent=test_parent_category_3, name='test_child_category_2',
                                event_type=EventType.CHANGE)

    def test_get_all_categories_no_auth(self):
        url = '/api/v1/categories/'

        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('results', response.data)

    def test_get_all_categories_as_user(self):
        user = User.objects.get(username='test_user_2')
        url = '/api/v1/categories/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('results', response.data)

    def test_get_all_categories_as_admin(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/categories/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 5)
        self.assertIn('results', response.data)
        self.assertEquals(response.data['results'][0]['user']['username'], 'test_user_1')
        self.assertEquals(response.data['results'][0]['name'], 'test_parent_category_1')
        self.assertEquals(response.data['results'][0]['event_type'], EventType.EXPENSE)
        self.assertNotIn('children', response.data['results'][0])

    def test_get_user_categories_no_auth(self):
        user_1 = User.objects.get(username='test_user_1')
        url = '/api/v1/users/' + user_1.username + '/categories/'

        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_categories_no_owner(self):
        user_1 = User.objects.get(username='test_user_1')
        user_2 = User.objects.get(username='test_user_2')
        url = '/api/v1/users/' + user_1.username + '/categories/'

        self.client.force_login(user_2)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_categories_as_owner(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/users/' + user.username + '/categories/'

        self.client.force_login(user)
        response = self.client.get(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['user']['username'], 'test_user_1')
        self.assertEquals(response.data[0]['name'], 'test_parent_category_1')
        self.assertEquals(response.data[0]['event_type'], EventType.EXPENSE)
        self.assertIn('children', response.data[0])
        self.assertEquals(len(response.data[0]['children']), 1)
        self.assertEquals(response.data[0]['children'][0]['name'], 'test_child_category_1')

    def test_post_category_no_auth(self):
        url = '/api/v1/categories/'
        new_category_name = 'test_parent_category_4'
        new_category_event_type = EventType.CHANGE
        data = {'name': new_category_name, 'event_type': new_category_event_type}

        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertFalse(CategoryViewSet.queryset.filter(name=new_category_name).exists())

    def test_post_category_auth_not_existing_event_type(self):
        user = User.objects.get(username='test_user_2')
        new_category_name = 'test_parent_category_4'
        url = '/api/v1/categories/'
        data = {'name': new_category_name, 'event_type': 'fake_type'}

        self.client.force_login(user)
        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('event_type', response.data)
        # test model
        self.assertFalse(CategoryViewSet.queryset.filter(name=new_category_name).exists())

    def test_post_category_auth_parent_event_type_not_matched(self):
        user = User.objects.get(username='test_user_2')
        parent = Category.objects.get(name='test_parent_category_3')
        new_category_name = 'test_child_category_3'
        new_category_event_type = EventType.INCOME
        url = '/api/v1/categories/'
        data = {'name': new_category_name, 'event_type': new_category_event_type, 'parent': parent.id}

        self.client.force_login(user)
        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Parent category event type does not match.', response.data['non_field_errors'])
        # test model
        self.assertFalse(CategoryViewSet.queryset.filter(name=new_category_name).exists())

    def test_post_category_auth_parent_user_not_matched(self):
        user = User.objects.get(username='test_user_2')
        parent = Category.objects.get(name='test_parent_category_1')
        new_category_name = 'test_child_category_3'
        new_category_event_type = EventType.EXPENSE
        url = '/api/v1/categories/'
        data = {'name': new_category_name, 'event_type': new_category_event_type, 'parent': parent.id}

        self.client.force_login(user)
        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Parent category user does not match.', response.data['non_field_errors'])
        # test model
        self.assertFalse(CategoryViewSet.queryset.filter(name=new_category_name).exists())

    def test_post_category_auth_circular_reference(self):
        user = User.objects.get(username='test_user_2')
        parent = Category.objects.get(name='test_parent_category_3')
        child = Category.objects.get(name='test_child_category_2')
        url = '/api/v1/categories/' + str(parent.id) + '/'
        data = {'parent': child.id}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Circular references are prohibited.', response.data['non_field_errors'])
        # test model
        self.assertIsNone(Category.objects.get(id=parent.id).parent)

    def test_post_category_auth(self):
        user = User.objects.get(username='test_user_2')
        new_category_name = 'test_parent_category_4'
        new_category_event_type = EventType.CHANGE
        url = '/api/v1/categories/'
        data = {'name': new_category_name, 'event_type': new_category_event_type}

        self.client.force_login(user)
        response = self.client.post(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(response.data), 8)    # number of serializer fields
        self.assertEquals(response.data['user']['username'], user.username)
        self.assertEquals(response.data['name'], new_category_name)
        self.assertEquals(response.data['event_type'], new_category_event_type)
        self.assertIsNone(response.data['parent'])
        self.assertTrue(response.data['root_node'])
        self.assertNotIn('children', response.data)
        # test model
        self.assertTrue(CategoryViewSet.queryset.filter(name=new_category_name).exists())
        self.assertEquals(CategoryViewSet.queryset.get(name=new_category_name).user.username, user.username)
        self.assertEquals(CategoryViewSet.queryset.get(name=new_category_name).event_type, new_category_event_type)
        self.assertIsNone(CategoryViewSet.queryset.get(name=new_category_name).parent)
        self.assertTrue(CategoryViewSet.queryset.get(name=new_category_name).root_node)

    def test_patch_category_no_auth(self):
        test_category = Category.objects.get(name='test_parent_category_3')
        new_category_name = 'patched_test_parent_category_3'
        url = '/api/v1/categories/' + str(test_category.id) + '/'
        data = {'name': new_category_name}

        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertEquals(CategoryViewSet.queryset.get(id=test_category.id).name, test_category.name)

    def test_patch_category_not_exist(self):
        user = User.objects.get(username='test_user_1')
        new_category_name = 'patched_test_parent_category_3'
        url = '/api/v1/categories/999/'
        data = {'name': new_category_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_category_no_owner(self):
        user = User.objects.get(username='test_user_1')
        test_category = Category.objects.get(name='test_parent_category_2')
        new_category_name = 'patched_test_parent_category_2'
        url = '/api/v1/categories/' + str(test_category.id) + '/'
        data = {'name': new_category_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertEquals(CategoryViewSet.queryset.get(id=test_category.id).name, test_category.name)

    def test_patch_tag_as_owner(self):
        user = User.objects.get(username='test_user_2')
        test_category = Category.objects.get(name='test_parent_category_2')
        new_category_name = 'patched_test_parent_category_2'
        url = '/api/v1/categories/' + str(test_category.id) + '/'
        data = {'name': new_category_name}

        self.client.force_login(user)
        response = self.client.patch(url, data)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 8)  # number of serializer fields
        self.assertEquals(response.data['id'], test_category.id)
        self.assertEquals(response.data['name'], new_category_name)
        self.assertEquals(response.data['event_type'], test_category.event_type)
        # test model
        self.assertEquals(CategoryViewSet.queryset.get(id=test_category.id).name, new_category_name)

    def test_delete_category_no_auth(self):
        test_category = Category.objects.get(name='test_parent_category_2')
        url = '/api/v1/categories/' + str(test_category.id) + '/'

        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertTrue(CategoryViewSet.queryset.filter(id=test_category.id).exists())

    def test_delete_category_not_exist(self):
        user = User.objects.get(username='test_user_1')
        url = '/api/v1/categories/999/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category_no_owner(self):
        user = User.objects.get(username='test_user_1')
        test_category = Category.objects.get(name='test_parent_category_2')
        url = '/api/v1/categories/' + str(test_category.id) + '/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        # test model
        self.assertTrue(CategoryViewSet.queryset.filter(id=test_category.id).exists())

    def test_delete_category_restrict_parent(self):
        user = User.objects.get(username='test_user_2')
        test_category = Category.objects.get(name='test_parent_category_3')
        url = '/api/v1/categories/' + str(test_category.id) + '/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertIn('Cannot delete category with subcategories.', response.data['detail'])
        # test model
        self.assertTrue(CategoryViewSet.queryset.filter(id=test_category.id).exists())

    def test_delete_tag_as_owner(self):
        user = User.objects.get(username='test_user_2')
        test_category = Category.objects.get(name='test_parent_category_2')
        url = '/api/v1/categories/' + str(test_category.id) + '/'

        self.client.force_login(user)
        response = self.client.delete(url)

        # test view and serializer
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        # test model
        self.assertFalse(CategoryViewSet.queryset.filter(id=test_category.id).exists())
