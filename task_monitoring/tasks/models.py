from django.core.validators import FileExtensionValidator
from django.db import models

from departments.models import Employee


class Group(models.Model):
    """Модель типа поручения."""

    name = models.CharField(
        verbose_name='Наименование типа поручения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип поручения'
        verbose_name_plural = 'Типы поручений'

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель Поручения."""
    
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=512
    )
    number = models.CharField(
        verbose_name='Номер поручения',
        max_length=56,
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Тип поручения',
        related_name='tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    initiator = models.ForeignKey(
        Employee,
        verbose_name='Инициатор',
        related_name='initiator_tasks',
        on_delete=models.CASCADE,
        db_index=True
    )
    resolution = models.TextField(
        verbose_name='Резолюция',
        max_length=10000
    )
    parent_task = models.ForeignKey(
        'self',
        verbose_name='Родительское поручение',
        related_name='redirected_tasks',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    executors = models.ManyToManyField(
        Employee,
        verbose_name='Исполнители',
        related_name='execution_tasks'
    )
    assignment_date = models.DateField(
        verbose_name='Дата поручения',
        auto_now_add=True,
        db_index=True
    )
    execution_date = models.DateField(
        verbose_name='Дата исполнения',
        db_index=True
    )
    is_closed = models.BooleanField(
        verbose_name='Отметка об исполнении поручения инициатором',
        default=False,
        db_index=True
    )
    is_completed = models.BooleanField(
        verbose_name='Отметка об исполнении поручения исполнителем',
        default=False,
        db_index=True
    )
    tasks_application = models.FileField(
        verbose_name='Приложение к поручению',
        upload_to='uploaded/tasks_files/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png']
            )
        ],
        help_text='Разрешенные расширения: doc, docx, pdf, jpg, jpeg, png.',
        blank=True,
        null=True
    )
    executions_application = models.FileField(
        verbose_name='Приложение к исполнению',
        upload_to='uploaded/applications/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png']
            )
        ],
        help_text='Разрешенные расширения: doc, docx, pdf, jpg, jpeg, png.',
        blank=True,
        null=True
    )
    executions_comment = models.TextField(
        verbose_name='Комментарий к исполнению',
        max_length=10000,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['execution_date']
        verbose_name = 'Поручение'
        verbose_name_plural = 'Поручения'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'number',
                    'initiator',
                    'assignment_date',
                ],
                name='unique_task'
            ),
        ]

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.initiator}'
