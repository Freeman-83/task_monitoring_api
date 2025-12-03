from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from departments.models import Employee, Department, ROLE_CHOICES


User = get_user_model()


class EmployeeTests(APITestCase):
    """Тестирование кейса Сотрудников."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        admin_token = 'admin_token'
        director_token = 'director_token'
        deputy_director_token = 'deputy_director_token'
        head_department_token = 'head_department_token_1'
        deputy_head_department_token = 'deputy_head_department_token'
        employee_token = 'employee_token_1'

        cls.admin_user = User.objects.create(
            email='admin@mail.ru',
            first_name='Админ',
            second_name='Админыч',
            last_name='Админов',
            is_staff=True
        )
        cls.director_user = User.objects.create(
            email='director@mail.ru',
            first_name='Иван',
            second_name='Иванович',
            last_name='Иванов',
        )
        cls.deputy_director_user = User.objects.create(
            email='deputy_director@mail.ru',
            first_name='Петр',
            second_name='Петрович',
            last_name='Петров'
        )
        cls.head_department_user = User.objects.create(
            email='head_department1@mail.ru',
            first_name='Сидор',
            second_name='Сидорович',
            last_name='Сидоров'
        )
        cls.deputy_head_department_user = User.objects.create(
            email='deputy_head_department@mail.ru',
            first_name='Глеб',
            second_name='Глебович',
            last_name='Глебов'
        )
        cls.employee_user = User.objects.create(
            email='employee1@mail.ru',
            first_name='Борис',
            second_name='Борисович',
            last_name='Борисов'
        )

        cls.guest_client = APIClient()
        cls.auth_admin = APIClient()
        cls.auth_director = APIClient()
        cls.auth_deputy_director = APIClient()
        cls.auth_head_department = APIClient()
        cls.auth_deputy_head_department = APIClient()
        cls.auth_employee = APIClient()

        cls.auth_admin.force_authenticate(
            cls.admin_user,
            admin_token
        )
        cls.auth_director.force_authenticate(
            cls.director_user,
            director_token
        )
        cls.auth_deputy_director.force_authenticate(
            cls.deputy_director_user,
            deputy_director_token
        )
        cls.auth_head_department.force_authenticate(
            cls.head_department_user,
            head_department_token
        )
        cls.auth_deputy_head_department.force_authenticate(
            cls.deputy_head_department_user,
            deputy_head_department_token
        )
        cls.auth_employee.force_authenticate(
            cls.employee_user,
            employee_token
        )

        cls.department = Department.objects.create(
            name='test department'
        )

        cls.admin_employee = Employee.objects.create(
            user=cls.admin_user,
            department=cls.department,
            role=ROLE_CHOICES[4][0]
        )
        cls.director_employee = Employee.objects.create(
            user=cls.director_user,
            role=ROLE_CHOICES[0][0]
        )
        cls.deputy_director_employee = Employee.objects.create(
            user=cls.deputy_director_user,
            role=ROLE_CHOICES[1][0]
        )
        cls.head_department_employee = Employee.objects.create(
            user=cls.head_department_user,
            department=cls.department,
            role=ROLE_CHOICES[2][0]
        )
        cls.deputy_head_department_employee = Employee.objects.create(
            user=cls.deputy_head_department_user,
            department=cls.department,
            role=ROLE_CHOICES[3][0]
        )
        cls.employee = Employee.objects.create(
            user=cls.employee_user,
            department=cls.department
        )

        cls.department.curator = cls.director_employee

        cls.employee_url = '/api/employees/'
        cls.department_url = '/api/departments/'


    def test_create_employee_admin_only(self):
        """Проверка прав на создание профиля сотрудника."""

        self.test_user = User.objects.create(
            email='test_user@mail.ru',
            first_name='Тест',
            second_name='Тест',
            last_name='Тест'
        )

        self.employee_data = {
            'user': self.test_user.id,
            'role': ROLE_CHOICES[1][0]
        }

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_201_CREATED
            ],
        }

        for response_subject, data in tests_data.items():
            self.assertEqual(
                response_subject.post(
                    EmployeeTests.employee_url, self.employee_data
                ).status_code,
                data[1],
                f'Статус запроса для "{data[0]}" не соответствует ожидаемому!'
            )


    def test_get_current_employee(self):
        """Проверка прав на просмотр профиля сотрудника."""

        current_user_url = EmployeeTests.employee_url + f'{EmployeeTests.head_department_employee.id}/'

        tests_data = {
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_200_OK
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_200_OK
            ],
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.get(current_user_url).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_partial_update_current_employee(self):
        """Проверка прав на изменение профиля сотрудника."""

        current_user_url = EmployeeTests.employee_url + f'{EmployeeTests.head_department_employee.id}/'

        changes_data = {'role': ROLE_CHOICES[1][0]}

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
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


    def test_delete_current_employee(self):
        """Проверка прав на удаление профиля сотрудника."""

        current_user_url = f'{EmployeeTests.employee_url}{EmployeeTests.head_department_employee.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
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
        """Проверка прав на создание нового подразделения."""

        self.department_data = {
            'name': 'test_department',
            'curator': EmployeeTests.director_employee.id
        }

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
            ],
            EmployeeTests.auth_admin: [
                'admin', status.HTTP_201_CREATED
            ]
        }

        for response_subject, response_status in tests_data.items():
            self.assertEqual(
                response_subject.post(
                    EmployeeTests.department_url,
                    data=self.department_data
                ).status_code,
                response_status[1],
                f'Статус запроса для "{response_status[0]}" не соответствует ожидаемому!'
            )


    def test_update_department(self):
        """Проверка прав на изменение данных о подразделении."""

        current_department_url = EmployeeTests.department_url + f'{EmployeeTests.department.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
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
        """Проверка прав на удаление данных о подразделении."""

        current_department_url = EmployeeTests.department_url + f'{EmployeeTests.department.id}/'

        tests_data = {
            EmployeeTests.auth_director: [
                'director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_director: [
                'deputy_director', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_head_department: [
                'head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_deputy_head_department: [
                'deputy_head_department', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.auth_employee: [
                'employee', status.HTTP_403_FORBIDDEN
            ],
            EmployeeTests.guest_client: [
                'guest_client', status.HTTP_401_UNAUTHORIZED
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
