import binascii
import os

from datetime import datetime, date
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from django.db.models import Q
from .utils import date_for_x_days_before_today
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class NuggetsToken(models.Model):
    """
    The default authorization token model.
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/models.py
    """
    # Switch key to textField since google token are > 1000 chars
    # Note that token length is constraint to 255 chars due to limitations of mysql.
    key = models.CharField(_("Key"), max_length=255, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='nuggets_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    given_name = models.TextField(null=True)
    family_name = models.TextField(null=True)
    profile_url = models.TextField(null=True)
    google_email = models.TextField(null=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(NuggetsToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def create_with_custom_token(cls, user, given_name, family_name, profile_url, google_email):
        return cls.objects.create(
            user=user,
            given_name=given_name,
            family_name=family_name,
            profile_url=profile_url,
            google_email=google_email)

    def __str__(self):
        return self.key


class Nugget(models.Model):
    source = models.TextField(null=False)
    content = models.TextField(null=False)
    url = models.TextField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_nuggets_by_user(cls, user, exclude_deleted=True):
        return [x.nugget for x in NuggetUser.get_nugget_users_by_user(user, exclude_deleted)]

    @classmethod
    def get_todays_review_nuggets_by_user(cls, user, exclude_deleted=True):
        return [x.nugget for x in NuggetUser.get_todays_review_nugget_users_by_user(user, exclude_deleted)]

    @classmethod
    def create_new_nugget(cls, user, content, source, url):
        nugget = cls.objects.create(
            creator=user,
            content=content,
            source=source,
            url=url)
        cls.add_existing_nugget(
            nugget=nugget,
            user=user,
            is_owner=True)
        return nugget

    @classmethod
    def delete_nugget(cls, user, nugget):
        NuggetUser.delete_nugget_user(user, nugget)
        Nugget.objects.filter(id=nugget.id).update(deleted_at=datetime.now())

    @classmethod
    def update_nugget(cls, user, nugget, new_nugget_content):
        Nugget.objects.filter(id=nugget.id, creator=user).update(content=new_nugget_content)

    @classmethod
    def add_existing_nugget(cls, nugget, user, is_owner=False):
        NuggetUser.add_new_nugget_for_user(
            nugget=nugget,
            user=user,
            is_owner=is_owner)

    @property
    def creator_name(self):
        return self.creator.username


class NuggetUser(models.Model):
    nugget = models.ForeignKey(Nugget, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_owner = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def add_new_nugget_for_user(cls, nugget, user, is_owner=False):
        return cls.objects.create(
            nugget=nugget,
            user=user,
            is_owner=is_owner)

    @classmethod
    def get_nugget_users_by_user(cls, user, exclude_deleted=True):
        q_objects = Q(user=user)
        if exclude_deleted:
            q_objects.add(Q(deleted_at__isnull=True), Q.AND)
        return cls.objects.filter(q_objects)

    @classmethod
    def get_todays_review_nugget_users_by_user(cls, user, exclude_deleted=True):
        review_interval_days = [0, 1, 3, 7, 14, 30, 90, 180, 360, 720]

        # elements of review_dates are of type <class 'datetime.date'>
        review_dates = [date_for_x_days_before_today(n) for n in review_interval_days]

        q_objects = Q(user=user)
        if exclude_deleted:
            q_objects.add(Q(deleted_at__isnull=True), Q.AND)

        # Note that Q(created_at__date__in=review_dates) doesn't cast
        # to datetime.date but to <datetime.datetime>
        # Note - seems inefficient to load all the nuggets for the user in
        # memory and filter them and we risk OOM-ing with large number of
        # nuggets. Better to rely on a database index.
        nuggetUserEntriesForReview = []
        for x in cls.objects.filter(q_objects):
            # dd is of type datetime.datetime and we need to
            # get the datetime.date from it
            if x.created_at.date() in review_dates:
                nuggetUserEntriesForReview.append(x)
        return nuggetUserEntriesForReview

    @classmethod
    def delete_nugget_user(cls, user, nugget):
        NuggetUser.objects.filter(user=user, nugget=nugget).update(deleted_at=datetime.now())
