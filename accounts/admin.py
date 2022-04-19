from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm
from .models import User, Message, Post, PostComment, Reply


class CustomUserAdmin (UserAdmin):
    add_form = RegistrationForm
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (
            'Fields', {
                'fields': ('email', 'first_name', 'last_name', 'street_num', 'city', 'state', 'zipcode', 'favoriteGenres', 'favoriteAuthors', 'wishlist', 'follow_list', 'profile_picture')
            },
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register (User, CustomUserAdmin)

class ReplyInlne(admin.StackedInline):
    model = Reply
    extra = 0

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'created_on']

    inlines = [
        ReplyInlne,
    ]

class MessageInline(admin.TabularInline):
    model = Message

class CommentInline(admin.StackedInline):
    model = PostComment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['writer', 'heading', 'created_on']
    inlines = [
        CommentInline,
    ]


