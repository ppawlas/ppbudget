from django.db import models
from django.contrib.auth.models import User
from dictionaries.models import EventType


class Category(models.Model):
    user = models.ForeignKey(User)
    parent = models.ForeignKey('self', default=None, blank=True, null=True)
    name = models.TextField(max_length=50)
    event_type = models.CharField(max_length=2, choices=EventType.EVENT_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.get_event_type_display())

    class Meta:
        unique_together = ('user', 'name', 'event_type')
