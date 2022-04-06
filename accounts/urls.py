from django.contrib.auth import views as auth_views
from django.urls import path, re_path


from . import views
app_name = 'accounts'

urlpatterns = [
    re_path (r'^customerView/$', views.customerView, name='customerView'),
    path('register/', views.registration_view.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('bookshelf/' ,views.myBookShelf, name='myBookShelf'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('viewProfile/<str:id>/', views.viewProfile, name='viewProfile'),
    path('editAddress/', views.edit_address, name='edit_address'),
    path('addBook/', views.addBook, name='addBook'),
    path('myFavBooks', views.viewFavBooks, name='viewFavBooks'),
    path('myFavAuthors', views.viewFavAuthors, name='viewFavAuthors'),
    path('myFavGenres', views.viewFavGenres, name='viewFavGenres'),
    path('addFavAuthor', views.addFavAuthors, name='addFavAuthors'),
    path('<int:pk>/delete', views.deleteBook, name='deleteBook'),
    path('<int:pk>/details', views.viewBook, name='viewBook'),
    path('<int:pk>/edit', views.edit_book, name='edit_book'),
    path('<int:pk>/changeVisibility', views.changeBookVisibility, name='changeBookVisibility'),
    path('findBook/', views.findBook, name='findBook'),
    path('<int:pk>/follow/', views.follow, name='follow'),
    path('<int:pk>/unfollow/', views.unfollow, name='unfollow'),
    path('myFollowings', views.followList, name='followList'),
    path('search/', views.search_results, name="search_results"),

]