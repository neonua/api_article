# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.

"""""""""

Modificate User
Create  manager model and NewUser class

"""""""""
# My User Manager
class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Input your email!')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password) # Using sha256
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# My User Model
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=u'email',
        max_length=255,
        unique=True,
        db_index=True
    )

    firstname = models.CharField(
        verbose_name=u'Sename',
        max_length=64,
        null=True,
        blank=True
    )

    lastname = models.CharField(
        verbose_name=u'Name',
        max_length=64,
        null=True,
        blank=True
    )
        # Activate user
    is_active = models.BooleanField(
        verbose_name=u'Active',
        default=True
    )

    is_admin = models.BooleanField(
        verbose_name=u'Superuser',
        default=False
    )

    def get_full_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'


# Signal. Create token after create user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Articles Model
class Post(models.Model):
    user_id = models.ForeignKey('User',
    verbose_name=u'ID User',
    null=True,
    blank=False,
    )

    title = models.CharField(
        verbose_name=u'Title',
        max_length=128,
        null=True,
        blank=False
    )

    body = models.TextField(
        verbose_name=u'Post body',
        null=True,
        blank=False
    )
    promo_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta(object):
        verbose_name = u'Post'
        verbose_name_plural = u'Posts'

    def __unicode__(self):
        return u'{0}'.format(self.title)