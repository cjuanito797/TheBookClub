# Generated by Django 4.0.2 on 2022-02-25 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_favorite_authors_user_favorite_books_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.CharField(default=False, max_length=5, validators=[django.core.validators.MinLengthValidator(5)]),
            preserve_default=False,
        ),
    ]
