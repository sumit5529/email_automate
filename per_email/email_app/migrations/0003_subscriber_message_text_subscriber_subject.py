# Generated by Django 4.2.7 on 2023-12-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0002_emailmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='message_text',
            field=models.CharField(default='text', max_length=255),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='subject',
            field=models.CharField(default='subject', max_length=255),
        ),
    ]
