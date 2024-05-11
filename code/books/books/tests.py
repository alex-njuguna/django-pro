from django.test import TestCase, Client
from django.urls import reverse

from .models import Book


class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title = 'After 4:30',
            author = 'Ben Maillu',
            price='10.00'
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, 'After 4:30')
        self.assertEqual(self.book.author, 'Ben Maillu')
        self.assertEqual(self.book.price, '10.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('books_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'After 4:30')
        self.assertTemplateUsed(response, 'books/books_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Ben Maillu')
        self.assertTemplateUsed(response, 'books/book_detail.html')
