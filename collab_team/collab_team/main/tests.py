from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class UserRegistrationTests(TestCase):

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
        })
        print(response.content)
        self.assertEqual(response.status_code, 302)
        form = response.context.get('form')
        print(form.errors)