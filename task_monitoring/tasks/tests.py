from datetime import datetime, date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from http import HTTPStatus

from tasks.models import Task, Group
from users.models import Department, ROLE_CHOICES


User = get_user_model()


class TaskTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.department = Department.objects.create(
            name='test department'
        )

        cls.guest_client = APIClient()

        cls.author = User.objects.create(
            email='author@mail.ru',
            first_name='Ivan',
            last_name='Ivanov',
            role=ROLE_CHOICES[1][0]
        )
        cls.department.curator = cls.author

        cls.executor = User.objects.create(
            email='executor1@mail.ru',
            first_name='Petr',
            last_name='Petrov',
            department=cls.department,
            role=ROLE_CHOICES[2][0]
        )
        cls.not_executor = User.objects.create(
            email='executor2@mail.ru',
            first_name='Sidor',
            last_name='Sidorov',
            department=cls.department,
            role=ROLE_CHOICES[3][0]
        )

        cls.auth_author = APIClient()
        cls.auth_author.force_login(cls.author)

        cls.auth_executor = APIClient()
        cls.auth_not_executor = APIClient()
        cls.auth_executor.force_login(cls.executor)
        cls.auth_not_executor.force_login(cls.not_executor)


    def setUp(self):
        self.group = Group.objects.create(
            name='test_group'
        )
        self.task_data = {
            'title': 'test task',
            'number': '1',
            'author': TaskTests.author,
            'group': self.group,
            'assignment_date': date.today(),
            'execution_date': date.today() + timedelta(days=4),
            'description': 'test description 1'
        }
        executor
        self.task = Task.objects.create(**self.task_data)
        self.task.executors.set([TaskTests.executor,])


    # def test_get_books(self):
    #     url = reverse('tasks')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    def test_get_groups(self):
        ...

    def test_get_tasks(self):
        ...

    def test_create_task(self):
        ...

    def test_redirect_task(self):
        ...




    def test_url_address_available(self):
        """Проверка доступности URL-адресов для разных пользователей."""
        users_urls_status = {
            TaskTests.guest_client:
            (   
                [f'/api/group/', status.HTTP_401_UNAUTHORIZED],
                [f'/api/tasks/', status.HTTP_401_UNAUTHORIZED],
                [f'/api/group/{self.group.id}/', status.HTTP_401_UNAUTHORIZED],
                [f'/api/tasks/{self.task.id}/', status.HTTP_401_UNAUTHORIZED],
                [f'/api/tasks/redirect_task/{TaskTests.not_executor}/', status.HTTP_401_UNAUTHORIZED]
            ),
            TaskTests.author:
            (
                ['/', HTTPStatus.OK],
                [f'/api/group/{self.group.id}/', status.HTTP_200_OK],
                [f'/api/tasks/{self.task.id}/', status.HTTP_200_OK],
                [f'/api/tasks/redirect_task/{TaskTests.not_executor}/', status.HTTP_302_FOUND]
            ),
            TaskTests.executor_1:
            (
                ['/', HTTPStatus.OK],
                [f'/api/group/{self.group.id}/', status.HTTP_200_OK],
                [f'/api/tasks/{self.task.id}/', status.HTTP_200_OK],
                [f'/api/tasks/redirect_task/{TaskTests.not_executor}/', status.HTTP_302_FOUND]
            ),
            TaskTests.executor_2:
            (
                ['/', HTTPStatus.OK],
                [f'/api/group/{self.group.id}/', status.HTTP_200_OK],
                [f'/api/tasks/{self.task.id}/', status.HTTP_200_OK],
                [f'/api/tasks/redirect_task/{TaskTests.not_executor}/', status.HTTP_302_FOUND]
            )
        }

        for client, url_response in users_urls_status.items():
            for url, response_status in url_response:
                with self.subTest(url=url):
                    response = client.get(url)
                    self.assertEqual(
                        response.status_code,
                        response_status,
                        (f'Статус запроса страницы {url}'
                         ' не соответствует ожидаемому')
                    )