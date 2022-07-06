from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.books.utils import get_book_image_upload_path
from apps.users.models import Author, Client


class Book(models.Model):
    authors = models.ManyToManyField(
        verbose_name=_("Authors"),
        to=Author,
        related_name="books",
        help_text=_("Choose authors or co-authors of the book")
    )
    name = models.CharField(
        verbose_name=_("Name of the book"),
        max_length=250
    )
    image = models.ImageField(
        verbose_name=_("Book image"),
        upload_to=get_book_image_upload_path
    )
    published_in = models.DateField(
        verbose_name=_("Date when the book was published")
    )
    description = models.TextField(
        verbose_name=_("More about the book"),
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "books"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
    """Books that client users borrow"""
    STILL_READING = 0
    FINISHED_READING = 1

    BOOK_STATUS_CHOICES = [
        (STILL_READING, _("Still Reading")),
        (FINISHED_READING, _("Finished Reading"))
    ]

    __current_status = None  # current status of the book

    client = models.ForeignKey(
        verbose_name=_("Client who is borrowing the book"),
        to=Client,
        on_delete=models.CASCADE,
        related_name="borrowed_books",
        related_query_name="borrowed_book"
    )
    book = models.ForeignKey(
        verbose_name=_("Book that is going be to borrowed"),
        to=Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        related_query_name="borrowing"
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Status of the borrowed books",
        choices=BOOK_STATUS_CHOICES,
        default=STILL_READING
    )
    date_finished = models.DateField(
        verbose_name="Date when the book has been finished reading",
        null=True   # if not finished yet
    )
    datetime_borred = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "borrowed_books"
        ordering = ["-datetime_borred"]

    def __str__(self):
        return self.client.user.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # self.status keeps new record that user is going to update here

        if (self.__current_status == self.STILL_READING and 
                self.status == self.FINISHED_READING):
            # recording date when book finished by check status change
            self.date_finished = date.today()
            self.__current_status = self.FINISHED_READING # setting current status
            
        elif (self.__current_status == self.FINISHED_READING and 
                self.status == self.STILL_READING):  
            # if book status has been changed from 'finished' to 'still reading'
            # set date_finished field back to null in the database 
            self.date_finished = None
            self.__current_status = self.STILL_READING  # setting current status

        super(BorrowedBook, self).save(force_insert, force_update, *args, **kwargs)
