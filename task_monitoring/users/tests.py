from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tasks.models import Task, Group
from users.models import Department, ROLE_CHOICES


User = get_user_model()


class CustomUserTests(APITestCase):
    """Тестирование кейса пользователей."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.admin_token = 'admin_token'
        cls.director_token = 'director_token'
        cls.head_department_token = 'head_department_token'

        cls.department = Department.objects.create(
            name='test department'
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
            first_name='Петр',
            second_name='Петрович',
            last_name='Петров',
            role=ROLE_CHOICES[0][0]
        )
        cls.head_department = User.objects.create(
            email='head_department@mail.ru',
            first_name='Сидор',
            second_name='Сидорович',
            last_name='Сидоров',
            role=ROLE_CHOICES[2][0],
            department=cls.department
        )

        cls.auth_admin = APIClient()
        cls.auth_director = APIClient()
        cls.auth_head_department = APIClient()

        cls.auth_admin.force_authenticate(
            cls.admin,
            token=cls.admin_token
        )
        cls.auth_director.force_authenticate(
            cls.director,
            cls.director_token
        )
        cls.auth_head_department.force_authenticate(
            cls.head_department,
            cls.head_department_token
        )

        cls.user_data = {
            'email': 'person@mail.ru',
            'first_name': 'Иван',
            'second_name': 'Иванович',
            'last_name': 'Иванов',
            'password': 'person_password',
            'role': ROLE_CHOICES[4][0],
            'department': cls.department.id
        }

        cls.create_user_url = '/api/users/'


    def test_create_user(self):
        """Проверка создания пользователя Админом."""

        response = CustomUserTests.auth_admin.post(
            CustomUserTests.create_user_url,
            CustomUserTests.user_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_user_token(self):
        """Проверка получения админом токена пользователя."""

        create_token_url = '/api/auth/token/login/'

        CustomUserTests.auth_admin.post(
            CustomUserTests.create_user_url,
            CustomUserTests.user_data
        )

        current_user = User.objects.get(email=CustomUserTests.user_data['email'])

        current_user_data = {
            'email': current_user.email,
            'password': CustomUserTests.user_data['password']
        }

        auth_current_user = APIClient()
        auth_current_user.force_login(current_user)

        response = CustomUserTests.auth_admin.post(
            create_token_url,
            current_user_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_current_user(self):
        """Проверка прав на получение профиля пользователя."""

        current_user_url = f'/api/users/{CustomUserTests.head_department.id}/'

        tests_data = {
            CustomUserTests.auth_head_department: [
                'head_department', status.HTTP_200_OK
            ],
            CustomUserTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            CustomUserTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.get(current_user_url).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_partial_update_current_user(self):
        """Проверка прав на изменение профиля пользователя."""

        current_user_url = f'/api/users/{CustomUserTests.head_department.id}/'

        changes_data = {'email': 'head_department_1@mail.ru'}

        tests_data = {
            CustomUserTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            CustomUserTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            CustomUserTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.patch(current_user_url, data=changes_data).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_delete_current_user(self):
        """Проверка прав на удаление профиля пользователя."""

        current_user_url = f'/api/users/{CustomUserTests.head_department.id}/'

        tests_data = {
            CustomUserTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            CustomUserTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            CustomUserTests.auth_admin: [
                'admin', status.HTTP_204_NO_CONTENT
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.delete(current_user_url).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )
    
