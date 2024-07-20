from django.test import TestCase
import base64

from main.services import search_city
from users.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.object = User.objects.create(
            first_name='Marta',
            email='marta.koshkina@gmail.com',
        )
        self.object.set_password('12345')
        self.object.save()

    def test_authorized(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
                                  base64.b64encode(b'email:password').decode("ascii")
        }
        response = self.client.get('/', **headers)
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        response = self.client.post('/register/')
        self.assertEqual(response.status_code, 200)
        new_user = User.objects.create(
            first_name='Marta',
            email='marta.okroshkina@gmail.com',
            password='marta.okroshkina2'
        )
        new_user.set_password('12345')
        new_user.save()
        login_user = self.client.login(email='marta.okroshkina@gmail.com', password='12345')
        self.assertTrue(login_user)
        self.assertEqual(new_user.email, 'marta.okroshkina@gmail.com')

    def test_user_detail_view(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.object.first_name, 'Marta')
        self.assertEqual(self.object.email, 'marta.koshkina@gmail.com')

    def test_user_update_view(self):
        response = self.client.post('/change_profile/')
        self.assertEqual(response.status_code, 302)
        self.object.first_name = 'Marina'
        self.object.email = 'marta.okroshkina@gmail.com'
        self.object.save()
        self.assertEqual(self.object.first_name, 'Marina')
        self.assertNotEqual(self.object.email, 'marta.koshkina@gmail.com')

    def test_user_delete_view(self):
        response = self.client.delete('/user_delete/')
        self.assertEqual(response.status_code, 302)
        self.object.delete()
        self.assertEqual(User.objects.count(), 0)

    def test_geosearch(self):
        self.assertEqual(search_city('"'), None)
        name, latitude, longitude = search_city('Москва')
        self.assertEqual(name, 'Москва')
