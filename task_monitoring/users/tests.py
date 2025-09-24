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

        admin_token = 'admin_token'

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

        cls.auth_admin = APIClient()
        cls.auth_admin.force_authenticate(
            cls.admin,
            token=admin_token
        )

        cls.user_data = {
            'email': 'director@mail.ru',
            'first_name': 'Иван',
            'second_name': 'Иванович',
            'last_name': 'Иванов',
            'password': 'director_password',
            'role': ROLE_CHOICES[0][0],
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

        url = '/api/auth/token/login/'

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

        response = CustomUserTests.auth_admin.post(url, current_user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
