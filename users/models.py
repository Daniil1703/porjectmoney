from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email адресс'), unique=True)
    first_name = models.CharField(_('Имя'), max_length=25, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=30, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('пользователя')
        verbose_name_plural = _('пользователей')

    def __str__(self):
         return self.email
