from django.apps import apps
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _


DIRECTOR = 'Директор'
DEPUTY_DIRECTOR = 'Заместитель директора'
HEAD_DEPARTMENT = 'Начальник отдела'
DEPUTY_HEAD_DEPARTMENT = 'Заместитель начальника отдела'
EMPLOYEE_DEPARTMENT = 'Сотрудник отдела'
ADMIN = 'Администратор'

ROLE_CHOICES = [
    (DIRECTOR, 'Директор'),
    (DEPUTY_DIRECTOR, 'Заместитель директора'),
    (HEAD_DEPARTMENT, 'Начальник отдела'),
    (DEPUTY_HEAD_DEPARTMENT, 'Заместитель начальника отдела'),
    (EMPLOYEE_DEPARTMENT, 'Сотрудник отдела'),
    (ADMIN, 'Администратор')
]


class CustomUserManager(UserManager):
    """Кастомный User Manager."""
    
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    

class Department(models.Model):
    """Модель Подразделения."""

    name = models.CharField(
        'Наименование',
        max_length=1000,
        unique=True
    )
    curator = models.ForeignKey(
        'CustomUser',
        related_name='subordinate_departments',
        verbose_name='Курирующий заместитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return f'{self.name}'


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    
    username = None
    email = models.EmailField(
        _('email'),
        max_length=254,
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
    chat_id = models.CharField(
        'id чата пользователя',
        max_length=100,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    role = models.CharField(
        'Статус',
        max_length=64,
        choices=ROLE_CHOICES,
        default=EMPLOYEE_DEPARTMENT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'email',
                    'first_name',
                    'last_name'
                ],
                name='unique_user'
            ),
        ]

    def is_director(self):
        return self.role == 'Директор'
    
    def is_deputy_director(self):
        return self.role == 'Заместитель директора'
    
    def is_head_department(self):
        return self.role == 'Начальник отдела'

    def is_deputy_head_department(self):
        return self.role == 'Заместитель начальника отдела'
    
    def is_employee(self):
        return self.role == 'Сотрудник отдела'
    
    def is_admin(self):
        return self.is_staff or self.role == 'Администратор'


    def __str__(self):
        return f'{self.last_name} {self.first_name}'
