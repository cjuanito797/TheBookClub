# Generated by Django 4.0.2 on 2022-04-25 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_sharebook_delete_requestbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='wishlist',
            field=models.BooleanField(default=False),
        ),
    ]
