from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse
from django.utils.text import slugify
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = MyUserManager()
    _TYPES_OF_USER = (
        ('client', 'Клиент'),
        ('specialist', 'Специалист'),
        ('other', 'Другой'),
    )
    type = models.CharField('Тип пользователя', max_length=10, choices=_TYPES_OF_USER, default='other')


class Category(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"pk": self.pk})


class City(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название города')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название района')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город района')

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.name


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    phone = models.IntegerField('Телефон')
    telegram = models.CharField('Телеграм', max_length=50)
    create_date = models.DateTimeField('Дата создания профиля', auto_now_add=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         ClientProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.client_profile.save()


class SpecialistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='specialists')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    phone = models.IntegerField('Телефон')
    telegram = models.CharField('Телеграм', max_length=50)
    create_date = models.DateTimeField('Дата создания профиля', auto_now_add=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    district = models.ForeignKey('District', on_delete=models.CASCADE, verbose_name='Район', blank=True, null=True)
    about = models.TextField('О себе', max_length=10000)

    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username, instance=self)
        super(SpecialistProfile, self).save(*args, **kwargs)