from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from tags.models import Tag
from dictionaries.models import EventType


class Resource(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(max_length=100)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.user.username)

    class Meta:
        unique_together = ('user', 'name')


class Event(models.Model):
    user = models.ForeignKey(User)
    description = models.TextField(max_length=500)
    event_type = models.CharField(max_length=2, choices=EventType.EVENT_TYPES)
    event_date = models.DateField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}: {2} ({3})'.format(self.event_date, self.get_event_type_display(), self.description,
                                             self.user.username)


class Operation(models.Model):
    event = models.ForeignKey(Event, related_name='operations')
    resource = models.ForeignKey(Resource)
    flow = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}: {2}'.format(self.event.description, self.resource.name, self.flow)
