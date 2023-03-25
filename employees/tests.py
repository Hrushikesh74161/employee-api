import base64
import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from employees.models import Employee
from employees import serializers


class EmployeeTests(APITestCase):
    def setUp(self) -> None:
        # employee data
        Employee.objects.create(name='Employee', age=32,
                                department='Sales', salary=40000, gender='M')
        Employee.objects.create(
            name='AnotherEmployee',
            age=25,
            department='Tech',
            salary=45000,
            gender='F'
        )

        # user for tests
        User.objects.create_user(
            email='testuser@email.com',
            username='testuser',
            password='testuser@1234'
        )
        self.user = User.objects.get(username='testuser')

        # authorization header
        user_auth = base64.b64encode(b'testuser:testuser@1234').decode('ascii')
        self.user_auth_header = {'HTTP_AUTHORIZATION': 'Basic ' + user_auth}

        admin_auth = base64.b64encode(b'admin:admin@1234').decode('ascii')
        self.admin_auth_header = {'HTTP_AUTHORIZATION': 'Basic ' + admin_auth}

    # test for get request for single employee, when authenticated
    def test_get_employee_authenticated(self):
        response = self.client.get(
            path='/api/employee/1',
            **self.user_auth_header
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['name'], 'Employee')

    # test for get request for single employee, when unauthenticated
    def test_get_employee_unauthenticated(self):
        response = self.client.get(path='/api/employee/1')
        self.assertEqual(response.status_code, 403)

    # test get request for employees
    def test_get_employees_authenticated(self):
        response = self.client.get(
            path='/api/employee',
            **self.user_auth_header
        )
        paginated_response = self.client.get(
            path='/api/employee?count=10&page=1',
            **self.user_auth_header
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['count'], Employee.objects.all().count())
        self.assertEqual(content['results'][0]['name'], 'Employee')
        self.assertNotEqual(content['results'][0]['name'], 'NotEmployee')

        # for paginated response
        paginated_content = json.loads(paginated_response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(paginated_content['count'], Employee.objects.all().count())
        self.assertEqual(paginated_content['results'][0]['name'], 'Employee')
        self.assertNotEqual(paginated_content['results'][0]['name'], 'NotEmployee')

    # test employee creation from authenticated user
    def test_create_employee_authenticated(self):
        data = {
            'name': 'testemployee',
            'age': 45,
            'gender': 'T',
            'department': 'Operations',
            'salary': 60000
        }
        data = json.dumps(data)
        response = self.client.post(
            path='/api/employee',
            data=data,
            content_type='application/json',
            **self.user_auth_header
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

    # test employee creation from unauthenticated user
    def test_create_employee_unauthenticated(self):
        data = {
            'name': 'otheremployee',
            'age': 45,
            'gender': 'T',
            'department': 'Operations',
            'salary': 60000
        }
        data = json.dumps(data)
        response = self.client.post(
            path='/api/employee',
            data=data,
            content_type='application/json',
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 403)


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testuser@1234',
        }
        self.data = json.dumps(data)
        self.url = '/api/register'

    # testing registering user with correct credentials
    def test_register_user(self):
        response = self.client.post(self.url, self.data, content_type='application/json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content['msg'], 'Registered Successfully')
        self.assertEqual(content['username'], 'testuser')

    # test for registering user with bad password
    def test_register_user_with_bad_password(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': '1234',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
