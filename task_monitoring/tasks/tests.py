from datetime import date, timedelta

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tasks.models import Task, Group
from users.models import Department, ROLE_CHOICES


User = get_user_model()


class TaskTests(APITestCase):
    """Тестирование кейса поручений."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        admin_token = 'admin_token'
        director_token = 'director_token'
        deputy_director_token = 'deputy_director_token'
        head_department_token_1 = 'head_department_token_1'
        head_department_token_2 = 'head_department_token_2'
        deputy_head_department_token = 'deputy_head_department_token'
        employee_token_1 = 'employee_token_1'
        employee_token_2 = 'employee_token_2'

        cls.department_1 = Department.objects.create(
            name='test department_1'
        )
        cls.department_2 = Department.objects.create(
            name='test department_2'
        )

        cls.admin = User.objects.create(
            email='admin@mail.ru',
            first_name='Админ',
            second_name='Админыч',
            last_name='Админов',
            role=ROLE_CHOICES[5][0],
            is_staff=True
        )
        cls.director = User.objects.create(
            email='director@mail.ru',
            first_name='Иван',
            second_name='Иванович',
            last_name='Иванов',
            role=ROLE_CHOICES[0][0]
        )
        cls.deputy_director = User.objects.create(
            email='deputy_director@mail.ru',
            first_name='Петр',
            second_name='Петрович',
            last_name='Петров',
            role=ROLE_CHOICES[1][0]
        )
        cls.head_department_1 = User.objects.create(
            email='head_department1@mail.ru',
            first_name='Сидор',
            second_name='Сидорович',
            last_name='Сидоров',
            role=ROLE_CHOICES[2][0],
            department=cls.department_1
        )
        cls.head_department_2 = User.objects.create(
            email='head_department2@mail.ru',
            first_name='Александр',
            second_name='Александрович',
            last_name='Александров',
            role=ROLE_CHOICES[2][0],
            department=cls.department_2
        )
        cls.deputy_head_department = User.objects.create(
            email='deputy_head_department@mail.ru',
            first_name='Глеб',
            second_name='Глебович',
            last_name='Глебов',
            role=ROLE_CHOICES[3][0],
            department=cls.department_1
        )
        cls.employee_1 = User.objects.create(
            email='employee1@mail.ru',
            first_name='Борис',
            second_name='Борисович',
            last_name='Борисов',
            department=cls.department_1
        )
        cls.employee_2 = User.objects.create(
            email='employee2@mail.ru',
            first_name='Антон',
            second_name='Антонович',
            last_name='Антонов',
            department=cls.department_2
        )

        cls.department_1.curator = cls.director
        cls.department_2.curator = cls.deputy_director

        cls.guest_client = APIClient()
        cls.auth_admin = APIClient()
        cls.auth_director = APIClient()
        cls.auth_deputy_director = APIClient()
        cls.auth_head_department_1 = APIClient()
        cls.auth_head_department_2 = APIClient()
        cls.auth_deputy_head_department = APIClient()
        cls.auth_employee_1 = APIClient()
        cls.auth_employee_2 = APIClient()

        cls.auth_admin.force_authenticate(
            cls.admin,
            admin_token
        )
        cls.auth_director.force_authenticate(
            cls.director,
            director_token
        )
        cls.auth_deputy_director.force_authenticate(
            cls.deputy_director,
            deputy_director_token
        )
        cls.auth_head_department_1.force_authenticate(
            cls.head_department_1,
            head_department_token_1
        )
        cls.auth_head_department_2.force_authenticate(
            cls.head_department_2,
            head_department_token_2
        )
        cls.auth_deputy_head_department.force_authenticate(
            cls.deputy_head_department,
            deputy_head_department_token
        )
        cls.auth_employee_1.force_authenticate(
            cls.employee_1,
            employee_token_1
        )
        cls.auth_employee_2.force_authenticate(
            cls.employee_2,
            employee_token_2
        )


    def setUp(self):
        self.group = Group.objects.create(
            name='test group 1'
        )
        task_data = {
            'title': 'test task 1',
            'number': '1',
            'author': TaskTests.admin,
            'group': self.group,
            'execution_date': date.today() + timedelta(days=4),
            'resolution': 'test resolution 1'
        }
        self.task = Task.objects.create(**task_data)
        self.task.executors.set([TaskTests.director, TaskTests.deputy_director])


    def test_get_groups(self):
        """Проверка прав на просмотр групп для Админа."""

        url = '/api/groups/'

        tests_data = {
            TaskTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            TaskTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_head_department_1: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_employee_1: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }

        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.get(url).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )


    def test_create_group(self):
        """Проверка прав на создание группы для Админа."""

        url = '/api/groups/'

        group_data = {'name': 'test group 2'}

        tests_data = {
            TaskTests.auth_admin: [
                'admin', status.HTTP_201_CREATED
            ],
            TaskTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_head_department_1: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.auth_employee_1: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }
        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.post(url, group_data).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )


    def test_get_tasks(self):
        """Проверка прав на просмотр поручений для разных пользователей."""

        url = '/api/tasks/'
        
        tests_data = {
            TaskTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            TaskTests.auth_director: [
                'director', status.HTTP_200_OK
            ],
            TaskTests.auth_deputy_director: [
                'deputy_director', status.HTTP_200_OK
            ],
            TaskTests.auth_head_department_1: [
                'head_department', status.HTTP_200_OK
            ],
            TaskTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_200_OK
            ],
            TaskTests.auth_employee_1: [
                'employee', status.HTTP_200_OK
            ],
            TaskTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }

        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.get(url).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )


    def test_get_current_task(self):
        """
        Проверка прав на просмотр поручения для инициатора и исполнителей
        и недоступности для остального персонала (кроме админа).
        """

        url = f'/api/tasks/{self.task.id}/'

        tests_data = {
            TaskTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            TaskTests.auth_director: [
                'director', status.HTTP_200_OK
            ],
            TaskTests.auth_deputy_director: [
                'deputy_director', status.HTTP_200_OK
            ],
            TaskTests.auth_head_department_1: [
                'head_department', status.HTTP_404_NOT_FOUND
            ],
            TaskTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_404_NOT_FOUND
            ],
            TaskTests.auth_employee_1: [
                'employee', status.HTTP_404_NOT_FOUND
            ],
            TaskTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }

        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.get(url).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )


    def test_create_task(self):
        """Проверка создания поручения и соответствующих прав."""

        url = '/api/tasks/'

        task_data = {
            'title': 'test task 2',
            'number': '2',
            'group': self.group.id,
            'execution_date': date.today() + timedelta(days=10),
            'resolution': 'test resolution 2',
            'executors': [TaskTests.employee_1.id]
        }

        tests_data = {
            TaskTests.auth_admin: [
                'admin', status.HTTP_201_CREATED
            ],
            TaskTests.auth_director: [
                'director', status.HTTP_201_CREATED
            ],
            TaskTests.auth_deputy_director: [
                'deputy_director', status.HTTP_201_CREATED
            ],
            TaskTests.auth_head_department_1: [
                'head_department_1', status.HTTP_201_CREATED
            ],
            TaskTests.auth_head_department_2: [
                'head_department_2', status.HTTP_400_BAD_REQUEST
            ],
            TaskTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_201_CREATED
            ],
            TaskTests.auth_employee_2: [
                'employee_2', status.HTTP_403_FORBIDDEN
            ],
            TaskTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }

        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.post(url, task_data).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )
            task_data['number'] = str(int(task_data['number']) + 1)


    def test_redirect_task(self):
        """Проверка создания перенаправление поручения и соответствующих прав."""

        url = '/api/tasks/{}/redirect_task/'

        response_executor_director = TaskTests.auth_director.post(
            url.format(self.task.id),
            {'executors': [TaskTests.deputy_director.id],
             'resolution': 'redirected_resolution'}
        )
        response_executor_deputy_director = TaskTests.auth_deputy_director.post(
            url.format(response_executor_director.data['id']),
            {'executors': [TaskTests.head_department_1.id],
             'resolution': 'redirected_resolution'}
        )
        response_executor_head_department_1 = TaskTests.auth_head_department_1.post(
            url.format(response_executor_deputy_director.data['id']),
            {'executors': [TaskTests.deputy_head_department.id],
             'resolution': 'redirected_resolution'}
        )
        response_executor_deputy_head_department = TaskTests.auth_deputy_head_department.post(
            url.format(response_executor_head_department_1.data['id']),
            {'executors': [TaskTests.employee_1.id],
             'resolution': 'redirected_resolution'}
        )
        response_not_executor = TaskTests.auth_head_department_2.post(
            url.format(response_executor_deputy_head_department.data['id']),
            {'executors': [TaskTests.employee_2.id],
             'resolution': 'redirected_resolution'}
        )
        response_head_department_for_not_curating_employee = TaskTests.auth_head_department_1.post(
            url.format(response_executor_deputy_head_department.data['id']),
            {'executors': [TaskTests.employee_2.id],
             'resolution': 'redirected_resolution'}
        )

        tests_data = {
            response_executor_director: [
                'director', status.HTTP_201_CREATED
            ],
            response_executor_deputy_director: [
                'deputy_director', status.HTTP_201_CREATED
            ],
            response_executor_head_department_1: [
                'head_department_1', status.HTTP_201_CREATED
            ],
            response_executor_deputy_head_department: [
                'deputy_head_department', status.HTTP_201_CREATED
            ],
            response_not_executor: [
                'not_executor', status.HTTP_404_NOT_FOUND
            ],
            response_head_department_for_not_curating_employee: [
                'head_department_for_not_curating_employee', status.HTTP_404_NOT_FOUND
            ]
        }

        for response, data in tests_data.items():
            self.assertEqual(
                response.status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )
