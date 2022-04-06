import datetime
import time

from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
import hashlib, random, sys
from django.core.validators import RegexValidator, MinLengthValidator
import django.utils.timezone

class Author (models.Model):
    first_name = models.CharField (max_length=50, db_index=True)
    last_name = models.CharField (max_length=50, db_index=True)
    slug = models.SlugField (max_length=200, db_index=True)
    favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ('last_name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse ('Library:author_detail', args=[self.id, self.slug])


class Genre (models.Model):
    name = models.CharField (max_length=200,
                             db_index=True, )
    slug = models.SlugField (max_length=200,
                             unique=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('Library:books_list_by_genre',
                        args=[self.slug]
                        )


class Book (models.Model):
    owner = models.ForeignKey ("accounts.User",
                                 related_name='owner',
                                 on_delete=models.CASCADE,
                                 default=None)
    genre = models.ForeignKey (Genre,
                               related_name='books',
                               on_delete=models.CASCADE)
    author = models.ForeignKey (Author,
                                related_name='books',
                                on_delete=models.CASCADE)
    title = models.CharField (max_length=50, db_index=True,)
    summary = models.TextField (blank=True)
    price = models.DecimalField (max_digits=10, decimal_places=2)
    available = models.BooleanField (default=True)
    slug = models.SlugField (max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13)])
    favorite = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)


    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('Library:book_detail',
                        args=[self.id, self.slug])



class requestBook(models.Model):
    borrower = models.ForeignKey ("accounts.User",
                                 related_name='book_borrower',
                                 on_delete=models.CASCADE,
                                 default=None)



    shared_on_date = models.DateField(default=time.timezone)
    shared_until = models.DateField()

    owner = models.ForeignKey("accounts.User",
                              related_name='book_owner',
                              on_delete=models.CASCADE,
                              default=None)
    approved = models.BooleanField(default=False)

    books = models.ManyToManyField (Book,
                                    related_name='Book',
                                    default=None,
                                    )

class followSystem(models.Model):
    this_user = models.OneToOneField("accounts.User",
                                     related_name='account_owner',
                                     on_delete=models.CASCADE,
                                     unique=True)

    following = models.ManyToManyField("accounts.User",
                                       related_name='following',
                                       )


