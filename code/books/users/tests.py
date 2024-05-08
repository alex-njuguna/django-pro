from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='Will',
            email='will@mail.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'Will')
        self.assertEqual(user.email, 'will@mail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@mail.com',
            password='testpass123'
        )

        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@mail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class RegisterPageTests(TestCase):

    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)

    def test_register_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/register.html')
        self.assertContains(self.response, 'Create an Account')
        self.assertNotContains(self.response, 'i dont belong here')