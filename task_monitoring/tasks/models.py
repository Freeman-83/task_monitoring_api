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
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Инициатор',
        on_delete=models.CASCADE,
        related_name='tasks_from'
    )
    responsible_executors = models.ManyToManyField(
        User,
        through='TaskUser',
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


class TaskUser(models.Model):
    """Модель отношений Задача - Исполнитель."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='in_users'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_tasks'
    )

    class Meta:
        verbose_name = 'Task - User'
        verbose_name_plural = 'Tasks - Users'
        constraints = [
            models.UniqueConstraint(
                fields=['task', 'user'],
                name='unique_task_for_user'
            )
        ]

    def __str__(self):
        return f'{self.task} - {self.user}'
