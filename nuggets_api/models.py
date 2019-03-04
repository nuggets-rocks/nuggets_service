from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Nugget(models.Model):
    source = models.TextField(null=False)
    content = models.TextField(null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True)

class Nugget_User(models.Model):
    nugget = models.ForeignKey(Nugget, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_owner = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
