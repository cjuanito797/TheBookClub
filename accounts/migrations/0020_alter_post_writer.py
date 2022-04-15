# Generated by Django 4.0.2 on 2022-04-15 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer', to=settings.AUTH_USER_MODEL),
        ),
    ]
