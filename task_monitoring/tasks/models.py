from django.core.validators import FileExtensionValidator
from django.db import models

from departments.models import Employee


class Document(models.Model):
    """Модель Документа."""

    document_application = models.FileField(
        verbose_name='',
        upload_to='docs/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png']
            )
        ],
        help_text='Разрешенные расширения: doc, docx, pdf, jpg, jpeg, png.',
        blank=True,
        null=True
    )


class Correspondence(Document):
    """Модель корреспонденции."""

    correspondence_type = models.CharField(
        verbose_name='Тип корреспонденции',
        max_length=56
    )
    registration_number = models.CharField(
        verbose_name='Номер регистрации',
        max_length=56
    )
    registration_date = models.DateField(
        verbose_name='Дата регистрации',
        auto_now_add=True,
        db_index=True
    )


class IncomingCorrespondence(Correspondence):
    """Входящая корреспонденция."""

    incoming_number = models.CharField(
        verbose_name='Входящий номер',
        max_length=56,
        blank=True,
        null=True
    )
    incoming_date = models.DateField(
        verbose_name='Входящая дата',
        auto_now_add=True,
        db_index=True
    )
    incoming_sender = models.CharField(
        verbose_name='Отправитель',
        max_length=56,
        blank=True,
        null=True
    )
    incoming_sender_person = models.CharField(
        verbose_name='Подписант',
        max_length=56,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.incoming_sender


class OutgoingCorrespondence(Correspondence):
    """Исходящая корреспонденция."""
    
    outgoing_sender_person = models.CharField(
        verbose_name='Подписант',
        max_length=56,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.outgoing_sender_person
    

class RegulatoryLegalAct(Document):
    """Модель номативно-правового акта."""

    title = outgoing_sender_person = models.CharField(
        verbose_name='Подписант',
        max_length=1000
    )
    rla_number = models.CharField(
        verbose_name='Номер',
        max_length=56
    )
    rla_date = models.DateField(
        verbose_name='Входящая дата',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.title


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
    task_application = models.ForeignKey(
        Document,
        verbose_name='Документация для исполнения',
        related_name='task_applications'
    )
    execution_application = models.ForeignKey(
        Document,
        verbose_name='Приложение к исполнению',
        related_name='execution_applications'
    )
    executions_comment = models.TextField(
        verbose_name='Комментарий к исполнению',
        max_length=10000,
        blank=True,
        null=True
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
