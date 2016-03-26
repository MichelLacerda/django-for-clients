from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Group, Permission,
    _user_has_perm, _user_has_module_perms, _user_get_all_permissions)
from cauth.utils import directory_path


class UserManager(BaseUserManager):
    """docstring for UserManager."""

    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            last_login=timezone.now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(email, password=password,
                                date_of_birth=date_of_birth)
        user.is_admin = True
        user.save(using=self._db)
        return user


class PermissionMixin(models.Model):
    """docstring for PermissionMixin."""

    PROFILE = (
        (0, 'Administrator'),
        (1, 'CEO'),
        (2, 'Agent'),
        (3, 'Customer'),
    )
    profile = models.PositiveSmallIntegerField(
        _('Profile'), choices=PROFILE, default=3)
    photo = models.ImageField(
        upload_to=directory_path,
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        related_query_name='user',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_(''),
        related_query_name='user',
        blank=True,
    )

    class Meta:
        """docstring for Meta."""

        abstract = True

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj)

    def has_module_perm(self, app_label):
        return _user_has_module_perms(self, app_label)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    @property
    def is_superuser(self):
        return self.is_admin


class User(AbstractBaseUser, PermissionMixin):
    """docstring for User."""

    email = models.EmailField(
        verbose_name=_('E-mail'),
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', ]

    class Meta:
        """docstring for Meta."""

        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (
            ('can_adm', 'Administrator'),
            ('can_ceo', 'CEO'),
            ('can_agent', 'Agent'),
            ('can_customer', 'Customer'),
        )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        else:
            return u'%s' % (self.first_name)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        """."""
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
