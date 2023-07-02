from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class ItemViewSetTestCase(APITestCase):
    url = '/game/items/'

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_unauthenticated_users_can_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_users_cannot_create_items(self):
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_users_can_create_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertNotEqual(response.status_code, 403)


class RarityViewSetTestCase(APITestCase):
    url = '/game/rarities/'

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_unauthenticated_users_can_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_users_cannot_create_items(self):
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_users_can_create_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertNotEqual(response.status_code, 403)


class GameViewSetTestCase(APITestCase):
    url = '/game/games/'

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_unauthenticated_users_can_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_users_cannot_create_items(self):
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_users_can_create_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, {'name': 'Test Item'}, format='json')
        self.assertNotEqual(response.status_code, 403)
