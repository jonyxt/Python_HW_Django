from django.shortcuts import render, get_list_or_404

from datetime import datetime
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {
        'books': Book.objects.all()
    }
    return render(request, template, context)

def pub_date_view(request, pub_date):
    template = 'books/books_date_list.html'
    pub_date = datetime.strptime(pub_date,"%Y-%m-%d").date()
    books = get_list_or_404(Book, pub_date=pub_date)
    books_dates = Book.objects.order_by('pub_date').values_list('pub_date', flat=True).distinct()
    current_index = list(books_dates).index(pub_date)
    prev_date = books_dates[current_index - 1] if current_index > 0 else None
    next_date = books_dates[current_index + 1] if current_index < len(books_dates) - 1 else None
    context = {
        'books': books,
        'current_date': pub_date,
        'prev_date': prev_date,
        'next_date': next_date
    }
    return render(request, template, context)