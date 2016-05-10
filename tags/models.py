from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        unique_together = ('user', 'name')
