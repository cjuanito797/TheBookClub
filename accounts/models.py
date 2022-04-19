from distutils import text_file
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from library.models import Book, Genre, Author
# Create your models here.
from .managers import CustomUserManager


class User (AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField (_ ('email'), unique=True)
    first_name = models.CharField (max_length=20)
    last_name = models.CharField (max_length=20)
    street_num = models.CharField (max_length=20)
    state = models.CharField (max_length=2)
    zipcode = models.CharField (max_length=5, validators=[MinLengthValidator (5)])
    city = models.CharField (max_length=20)
    is_staff = models.BooleanField (default=False)
    is_active = models.BooleanField (default=True)
    date_joined = models.DateTimeField (default=timezone.now)
    favoriteGenres = models.ManyToManyField (Genre, symmetrical=False, blank=True)
    favoriteAuthors = models.ManyToManyField (Author, blank=True)
    follow_list = models.ManyToManyField ('accounts.User', blank=True)
    bio = models.TextField (blank=True)
    wishlist = models.ManyToManyField (Book, symmetrical=False, blank=True)
    profile_picture = models.ImageField (upload_to='users/%Y/%m/%d',
                                         blank=True)
    objects = CustomUserManager ( )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email


class Message (models.Model):
    sender = models.ForeignKey ('accounts.User', related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey ('accounts.User', related_name='reciever', on_delete=models.CASCADE)
    message = models.TextField ( )
    created_on = models.DateTimeField (auto_now_add=True)


class Post (models.Model):
    writer = models.ForeignKey ('accounts.User', related_name='writer', on_delete=models.CASCADE)
    heading = models.CharField (max_length=30, blank=False, null=False)
    content = models.TextField ( )
    created_on = models.DateTimeField (auto_now_add=True)


Post.objects.order_by ("created_on")
