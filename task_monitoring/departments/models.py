from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


DIRECTOR = 'Директор'
DEPUTY_DIRECTOR = 'Заместитель директора'
HEAD_DEPARTMENT = 'Начальник отдела'
DEPUTY_HEAD_DEPARTMENT = 'Заместитель начальника отдела'
EMPLOYEE = 'Сотрудник отдела'
ADMIN = 'Администратор'

ROLE_CHOICES = [
    (DIRECTOR, 'Директор'),
    (DEPUTY_DIRECTOR, 'Заместитель директора'),
    (HEAD_DEPARTMENT, 'Начальник отдела'),
    (DEPUTY_HEAD_DEPARTMENT, 'Заместитель начальника отдела'),
    (EMPLOYEE, 'Сотрудник отдела'),
    (ADMIN, 'Администратор')
]


class Department(models.Model):
    """Модель Подразделения."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=1000,
        unique=True
    )
    curator = models.ForeignKey(
        User,
        verbose_name='Куратор',
        related_name='subordinate_departments',
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


class Employee(models.Model):
    """Модель Сотрудника организации."""

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        related_name='employee',
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        verbose_name='Подразделение',
        related_name='employees',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    role = models.CharField(
        verbose_name='Должность',
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[4][0]
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def is_admin(self):
        return self.user.is_staff

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

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'
