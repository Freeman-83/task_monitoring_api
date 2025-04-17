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

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    """Модель Задачи."""

    title = models.CharField(
        'Заголовок',
        max_length=512
    )
    description = models.TextField(
        'Описание',
        max_length=10000
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_from'
    )
    group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
        verbose_name='Группа',
    )
    assignment_date = models.DateTimeField(
        'Дата поручения',
        auto_now_add=True
    )
    execution_date = models.DateTimeField(
        'Дата исполнения',
    )
    responsible_executor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_for'
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

    def __str__(self) -> str:
        return self.title
