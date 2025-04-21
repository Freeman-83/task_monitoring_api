from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    """Модель типа задачи."""

    name = models.CharField(
        'Ниманование типа задачи',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель Задачи."""

    COMPLETED = 'completed'
    ON_EXECUTION = 'on_execution'

    EXECUTION_STATUS = (
        (COMPLETED, 'исполнено'),
        (ON_EXECUTION, 'на исполнении')
    )

    title = models.CharField(
        'Заголовок',
        max_length=512
    )
    description = models.TextField(
        'Описание',
        max_length=10000
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Тип поручения',
        related_name='tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Инициатор',
        related_name='tasks_from',
        on_delete=models.CASCADE
    )
    executors = models.ManyToManyField(
        User,
        related_name='tasks',
        verbose_name='Исполнители'
    )
    assignment_date = models.DateField(
        'Дата поручения',
        auto_now_add=True,
        db_index=True
    )
    execution_date = models.DateField(
        'Дата исполнения',
        db_index=True
    )
    execution_status = models.CharField(
        'Статус исполнения',
        choices=EXECUTION_STATUS,
        default=ON_EXECUTION
    )

    class Meta:
        ordering = ['assignment_date']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'assignment_date',
                ],
                name='unique_task'
            ),
        ]

    def __str__(self):
        return self.title



