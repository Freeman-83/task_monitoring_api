from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True
    )
    chat_id = models.CharField(
        'id чата пользователя',
        max_length=100,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'username',
                    'first_name',
                    'last_name'
                ],
                name='unique_user'
            ),
        ]

    def __str__(self):
        return self.username
