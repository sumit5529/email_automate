# Generated by Django 4.2.7 on 2023-12-07 20:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0007_alter_nextemailhistory_schedule_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='message_text',
        ),
        migrations.RemoveField(
            model_name='subscriber',
            name='subject',
        ),
        migrations.AlterField(
            model_name='nextemailhistory',
            name='schedule_time',
            field=models.TimeField(default=datetime.time(1, 35, 59, 550791)),
        ),
        migrations.CreateModel(
            name='EmailPlusScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='subject', max_length=255)),
                ('message_text', models.CharField(default='text', max_length=255)),
                ('schedule_time', models.TimeField()),
                ('gap', models.IntegerField()),
                ('frequency', models.IntegerField()),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.subscriber')),
            ],
        ),
    ]