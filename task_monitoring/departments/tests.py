from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tasks.models import Task, Group
from departments.models import Employee, Department, ROLE_CHOICES


User = get_user_model()


class EmployeeTests(APITestCase):
    """Тестирование кейса сотрудников."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.admin_token = 'admin_token'
        cls.director_token = 'director_token'
        cls.head_department_token = 'head_department_token'


        cls.admin = User.objects.create(
            email='admin@mail.ru',
            first_name='Админ',
            second_name='Админыч',
            last_name='Админов',
            is_staff=True
        )
        cls.director_user = User.objects.create(
            email='director@mail.ru',
            first_name='Петр',
            second_name='Петрович',
            last_name='Петров'
        )

        cls.head_department_user = User.objects.create(
            email='head_department@mail.ru',
            first_name='Сидор',
            second_name='Сидорович',
            last_name='Сидоров'
        )


        cls.auth_admin = APIClient()
        cls.auth_director = APIClient()
        cls.auth_head_department = APIClient()

        cls.auth_admin.force_authenticate(
            cls.admin,
            token=cls.admin_token
        )
        cls.auth_director.force_authenticate(
            cls.director_user,
            cls.director_token
        )
        cls.auth_head_department.force_authenticate(
            cls.head_department_user,
            cls.head_department_token
        )


        cls.director_employee = Employee.objects.create(
            user=cls.director_user,
            role=ROLE_CHOICES[0][0]
        )
        cls.department = Department.objects.create(
            name='test department',
            curator=cls.director_employee
        )
        cls.head_department_employee = Employee.objects.create(
            user=cls.head_department_user,
            department=cls.department,
            role=ROLE_CHOICES[2][0]
        )


        cls.employee_data = {
            'user': cls.director_user.id,
            'role': ROLE_CHOICES[0][0]
        }
        cls.department_data = {
            'name': 'test_department',
            'curator': cls.director_employee.id
        }


        cls.create_employee_url = '/api/employees/'
        cls.create_department_url = '/api/departments/'


    def test_create_employee(self):
        """Проверка создания сотрудника Админом."""

        response = EmployeeTests.auth_admin.post(
            EmployeeTests.create_user_url,
            EmployeeTests.employee_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_current_employee(self):
        """Проверка прав на просмотр профиля сотрудника."""

        current_user_url = f'/api/employees/{EmployeeTests.head_department_employee.id}/'

        tests_data = {
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_200_OK
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            EmployeeTests.auth_director: [
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
        """Проверка прав на изменение профиля сотрудника."""

        current_user_url = f'/api/employees/{EmployeeTests.head_department_employee.id}/'

        changes_data = {'role': ROLE_CHOICES[1][0]}

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_admin: [
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
        """Проверка прав на удаление профиля сотрудника."""

        current_user_url = f'/api/employees/{EmployeeTests.head_department_employee.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_204_NO_CONTENT
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.delete(current_user_url).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )
    

    def test_create_department(self):
        """Проверка прав на создание нового отдела только для админа."""

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_201_CREATED
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.post(
                    EmployeeTests.create_department_url,
                    data=EmployeeTests.department_data
                ).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_update_department(self):
        """Проверка прав на изменение данных об отделе только для админа."""

        current_department_url = f'/api/departments/{EmployeeTests.department.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.patch(
                    current_department_url,
                    data={'curator': EmployeeTests.head_department_employee.id}
                ).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_delete_department(self):
        """Проверка прав на удаление данных об отделе только для админа."""

        current_department_url = f'/api/departments/{EmployeeTests.department.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_204_NO_CONTENT
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.delete(current_department_url).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )
