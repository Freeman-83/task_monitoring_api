from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
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

        admin_token = 'admin_token'
        director_token = 'director_token'
        deputy_director_token = 'deputy_director_token'
        head_department_token = 'head_department_token'
        deputy_head_department_token = 'deputy_head_department_token'
        employee_token = 'employee_token'

        cls.admin = User.objects.create(
            email='admin@mail.ru',
            first_name='Admin',
            last_name='Adminov',
            role=ROLE_CHOICES[5][0],
            is_staff=True
        )
        cls.director = User.objects.create(
            email='director@mail.ru',
            first_name='Ivan',
            last_name='Ivanov',
            role=ROLE_CHOICES[0][0]
        )
        cls.deputy_director = User.objects.create(
            email='deputy_director@mail.ru',
            first_name='Petr',
            last_name='Petrov',
            role=ROLE_CHOICES[1][0]
        )
        cls.head_department = User.objects.create(
            email='head_department@mail.ru',
            first_name='Sidor',
            last_name='Sidorov',
            role=ROLE_CHOICES[2][0]
        )
        cls.deputy_head_department = User.objects.create(
            email='deputy_head_department@mail.ru',
            first_name='Gleb',
            last_name='Glebov',
            role=ROLE_CHOICES[3][0]
        )
        cls.employee = User.objects.create(
            email='employee@mail.ru',
            first_name='Boris',
            last_name='Borisov',
            role=ROLE_CHOICES[4][0]
        )

        cls.department_1 = Department.objects.create(
            name='test department_1'
        )
        cls.department_2 = Department.objects.create(
            name='test department_2'
        )
        cls.department_1.curator = cls.director
        cls.department_2.curator = cls.deputy_director

        cls.guest_client = APIClient()
        cls.auth_admin = APIClient()
        cls.auth_director = APIClient()
        cls.auth_deputy_director = APIClient()
        cls.auth_head_department = APIClient()
        cls.auth_deputy_head_department = APIClient()
        cls.auth_employee = APIClient()

        cls.auth_admin.force_authenticate(
            cls.admin, token=admin_token
        )
        cls.auth_director.force_authenticate(
            cls.director, token=director_token
        )
        cls.auth_deputy_director.force_authenticate(
            cls.deputy_director, token=deputy_director_token
        )
        cls.auth_head_department.force_authenticate(
            cls.head_department, token=head_department_token
        )
        cls.auth_deputy_head_department.force_authenticate(
            cls.deputy_head_department, token=deputy_head_department_token
        )
        cls.auth_employee.force_authenticate(
            cls.employee, token=employee_token
        )


    def setUp(self):
        self.group = Group.objects.create(
            name='test_group'
        )
        task_data = {
            'title': 'test task 1',
            'number': '1',
            'author': TaskTests.director,
            'group': self.group,
            'execution_date': date.today() + timedelta(days=4),
            'description': 'test description 1'
        }
        self.task = Task.objects.create(**task_data)
        self.task.executors.set(
            [TaskTests.deputy_director, TaskTests.head_department]
        )


    def test_get_groups(self):
        """Проверка доступности url групп для Админа."""

        url = '/api/groups/'
        response = TaskTests.auth_admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_tasks(self):
        """Проверка доступности url поручений для разных пользователей."""

        url = '/api/tasks/'
        director_response = TaskTests.auth_director.get(url)
        deputy_director_response = TaskTests.auth_director.get(url)
        head_department_response = TaskTests.auth_head_department.get(url)

        self.assertEqual(
            director_response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            deputy_director_response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            head_department_response.status_code, status.HTTP_200_OK
        )


    def test_create_task(self):
        url = '/api/tasks/'
        task_data = {
            'title': 'test task 2',
            'number': '2',
            'group': self.group.id,
            'execution_date': date.today() + timedelta(days=10),
            'description': 'test description 2',
            'executors': [TaskTests.deputy_director.id, TaskTests.head_department.id]
        }
        response = TaskTests.auth_director.post(url, task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_redirect_task(self):
        url = f'/api/tasks/{self.task.id}/redirect_task/'

        response = TaskTests.auth_deputy_director.post(
            url, data={'executors': [TaskTests.deputy_head_department.id]}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
