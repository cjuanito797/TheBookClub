from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.Signup, name='Signup'),
]