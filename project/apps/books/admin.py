from django.contrib import admin

from apps.books.models import (
    Book, 
    BorrowedBook
)


admin.site.register(Book)
admin.site.register(BorrowedBook)
