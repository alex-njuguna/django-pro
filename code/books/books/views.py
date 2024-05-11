from django.shortcuts import render

from .models import Book


def books_list(request):
    books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books, 'title': 'books'})

def book_detail(request, id):
    book = Book.objects.get(id)
    return render(request, 'books/book_detail.html', {'book': book, 'title': book.title})
