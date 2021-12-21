from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    _TYPES_OF_USER = (
        ('client', 'Клиент'),
        ('specialist', 'Специалист'),
        ('other', 'Другой'),
    )
    type = models.CharField(max_length=10, choices=_TYPES_OF_USER, default='other')


class ClientProfile(models.Model):
    pass


class SpecialistProfile(models.Model):
    pass

