from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        url = '/auth/token/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_authenticated_endpoint(self):
        url = '/auth/user-details/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class RegisterUserAPIViewTestCase(APITestCase):
    url = '/auth/register/'

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
