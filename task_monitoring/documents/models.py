from django.core.validators import FileExtensionValidator
from django.db import models

from departments.models import Employee


class DocumentType(models.Model):
    """Модель Типа документа."""

    name = models.CharField(
        verbose_name='Тип документа',
        max_length=56
    )

    def __str__(self):
        return self.name


class Document(models.Model):
    """Базовая модель Документа."""

    document_type = models.ForeignKey(
        DocumentType,
        verbose_name='Тип документа',
        related_name='documents',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    title = models.CharField(
        verbose_name='Наименование',
        max_length=500
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
    execution_date = models.DateField(
        verbose_name='Дата исполнения',
        db_index=True
    )
    task_application = models.FileField(
        verbose_name='',
        upload_to='task_application/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png']
            )
        ],
        help_text='Разрешенные расширения: doc, docx, pdf, jpg, jpeg, png.',
        blank=True,
        null=True
    )
    execution_application = models.FileField(
        verbose_name='',
        upload_to='execution_application/',
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
    is_closed = models.BooleanField(
        verbose_name='Отметка об исполнении инициатором',
        default=False,
        db_index=True
    )
    is_completed = models.BooleanField(
        verbose_name='Отметка об исполнении исполнителем',
        default=False,
        db_index=True
    )

    class Meta:
        ordering = ['execution_date']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'registration_number',
                    'initiator',
                    'registration_date',
                ],
                name='unique_task'
            ),
        ]

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.initiator}'





class Document(Task):
    """Модель Документа."""

    
    signatory = models.CharField(
        verbose_name='Подписант',
        max_length=56,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.title} - {self.signatory}'


class Correspondence(Document):
    """Модель корреспонденции."""

    def __str__(self):
        return f'{self.title} - {self.signatory}'


class IncomingCorrespondence(Correspondence):
    """Модель Входящей корреспонденции."""

    document_number = models.CharField(
        verbose_name='Номер документа',
        max_length=56,
        blank=True,
        null=True
    )
    document_date = models.DateField(
        verbose_name='Дата документа',
        auto_now_add=True,
        db_index=True
    )
    sender = models.CharField(
        verbose_name='Отправитель',
        max_length=500
    )

    class Meta:
        ordering = ['registration_date']
        verbose_name = 'Входящий документ'
        verbose_name_plural = 'Входящие'

    def __str__(self):
        return f'{self.title} - {self.sender} {self.signatory}'


class OutgoingCorrespondence(Correspondence):
    """Модель Исходящей корреспонденции."""

    addressee = models.CharField(
        verbose_name='Адресат',
        max_length=500
    )

    class Meta:
        ordering = ['registration_date']
        verbose_name = 'Исходящий документ'
        verbose_name_plural = 'Исходящие'

    def __str__(self):
        return f'{self.title} - {self.signatory}'


class InternalCorrespondence(Correspondence):
    """Модель Внутренней корреспонденции."""

    sender_employee = models.ForeignKey(
        Employee,
        verbose_name='Автор',
        related_name='internal_outgoing_correcpondence',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    addressee_employee = models.ForeignKey(
        Employee,
        verbose_name='Адресат',
        related_name='internal_incoming_correcpondence',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['registration_date']
        verbose_name = 'Внутренний документ'
        verbose_name_plural = 'Внутренние'

    def __str__(self):
        return f'{self.sender_employee} - {self.addressee_employee}'


class OrganizationalAdministrativeDocumentation(Document):
    """Модель организационно-распорядительной документации (ОРД)."""

    ...


class Assignment(Task):
    """Модель Поручения."""

    class Meta:
        ordering = ['execution_date']
        verbose_name = 'Поручение'
        verbose_name_plural = 'Поручения'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'registration_number',
                    'initiator',
                    'registration_date',
                ],
                name='unique_assignment'
            ),
        ]

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.initiator}'

# Create your models here.
