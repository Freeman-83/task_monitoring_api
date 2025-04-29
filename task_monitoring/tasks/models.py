from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


User = get_user_model()


COMPLETED = 'completed'
ON_EXECUTION = 'on_execution'
URGENT = 'urgent'
OVERDUE = 'overdue'

EXECUTION_STATUS = (
    (COMPLETED, 'исполнено'),
    (ON_EXECUTION, 'на исполнении'),
    (URGENT, 'срочное'),
    (OVERDUE, 'просрочено')
)


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
    
    title = models.CharField(
        'Заголовок',
        max_length=512
    )
    number = models.CharField(
        'Номер поручения',
        max_length=56,
        blank=True,
        null=True
    )
    assignment_date = models.DateField(
        'Дата поручения',
        auto_now_add=True,
        db_index=True
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
    parent_task = models.ForeignKey(
        'self',
        verbose_name='Перенаправлено от',
        related_name='redirected_tasks',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    executors = models.ManyToManyField(
        User,
        related_name='tasks',
        verbose_name='Исполнители'
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
    tasks_file = models.FileField(
        'Приложение',
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

    class Meta:
        ordering = ['execution_date']
        verbose_name = 'Поручение'
        verbose_name_plural = 'Поручения'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'author',
                    'assignment_date',
                ],
                name='unique_task'
            ),
        ]

    def __str__(self):
        return f'{self.title} - {self.author}'



