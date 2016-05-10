from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User
from dictionaries.models import EventType
from categories.models import Category
from tags.models import Tag
from events.models import Resource, Operation, Event


class EventTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_user')
        test_category = Category.objects.create(user=test_user, name='test_category', event_type=EventType.EXPENSE)

        event = Event.objects.create(
            user=test_user, description='test_description_1', event_type=EventType.EXPENSE,
            event_date=date.today(), category=test_category
        )

        test_tag_1 = Tag.objects.create(user=test_user, name='test_tag_1')
        test_tag_2 = Tag.objects.create(user=test_user, name='test_tag_2')

        event.tags.add(test_tag_1)
        event.tags.add(test_tag_2)

        test_resource_1 = Resource.objects.create(user=test_user, name='test_resource_1', initial_balance=99.99)
        test_resource_2 = Resource.objects.create(user=test_user, name='test_resource_2', initial_balance=199.99)

        Operation.objects.create(event=event, resource=test_resource_1, flow=-9.99)
        Operation.objects.create(event=event, resource=test_resource_2, flow=-29.99)

    def test_event_model(self):
        event = Event.objects.get(description='test_description_1')

        self.assertEquals(event.user.username, 'test_user')
        self.assertEquals(event.description, 'test_description_1')
        self.assertEquals(event.event_type, EventType.EXPENSE)
        self.assertEquals(event.event_date, date.today())
        self.assertEquals(event.category.name, 'test_category')
        self.assertEquals(len(event.tags.all()), 2)
        self.assertIsNotNone(event.tags.get(name='test_tag_2'))
        self.assertEquals(len(event.operations.all()), 2)
        self.assertEquals(event.operations.get(flow=-9.99).resource.name, 'test_resource_1')
