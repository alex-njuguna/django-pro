from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Book


@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books, 'title': 'books'})

@login_required
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_detail.html', {'book': book, 'title': book.title})
