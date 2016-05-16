from django.db import models
from django.db.models.deletion import ProtectedError
from django.contrib.auth.models import User
from dictionaries.models import EventType
from rest_framework import exceptions


class Category(models.Model):
    user = models.ForeignKey(User)
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    event_type = models.CharField(max_length=2, choices=EventType.EVENT_TYPES)
    root_node = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.parent:
            self.root_node = False
        else:
            self.root_node = True

        return super(Category, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        try:
            return super(Category, self).delete(using, keep_parents)
        except ProtectedError:
            # TODO check and try to distinguish the deletion when dependent events exist
            raise exceptions.ParseError('Cannot delete category with subcategories.')

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.get_event_type_display())

    class Meta:
        unique_together = ('user', 'name', 'event_type')
