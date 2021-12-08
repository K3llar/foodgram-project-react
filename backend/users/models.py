from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


CHOICES = {
    'user': 'user',
    'moderator': 'moderator',
    'admin': 'admin',
}


class User(AbstractUser):
    email = models.EmailField(verbose_name=_('email address'),
                              unique=True)
    username = models.CharField(verbose_name=_('username'),
                                max_length=20,
                                unique=True)
    first_name = models.CharField(verbose_name=_('first name'),
                                  max_length=20)
    last_name = models.CharField(verbose_name=_('last name'),
                                 max_length=30)
    role = models.CharField(verbose_name=_('статус'),
                            max_length=20,
                            choices=CHOICES.items(),
                            default=CHOICES['user'])
    date_joined = models.DateTimeField(
        verbose_name=_('Дата регистрации'),
        auto_now_add=True,
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.is_staff or self.role == CHOICES['moderator']

    @property
    def is_admin(self):
        return self.is_superuser or self.role == CHOICES['admin']
