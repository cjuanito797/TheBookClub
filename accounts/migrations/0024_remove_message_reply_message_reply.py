# Generated by Django 4.0.2 on 2022-04-19 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_message_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='reply',
        ),
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.ManyToManyField(blank=True, null=True, related_name='reply_message', to='accounts.Message'),
        ),
    ]