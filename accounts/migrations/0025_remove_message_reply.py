# Generated by Django 4.0.2 on 2022-04-19 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_remove_message_reply_message_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='reply',
        ),
    ]