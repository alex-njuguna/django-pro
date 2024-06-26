from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import home, about


class HomePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Homepage')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'I shoould not be here')

    def test_homepage_url_resolves_home(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, home.__name__)
        

class AboutPageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'About Page')

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Dont belong here')

    def test_aboutpage_url_resolves_about_view(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, about.__name__)
        