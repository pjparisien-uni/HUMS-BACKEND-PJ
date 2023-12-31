# Generated by Django 4.1.7 on 2023-04-06 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='dateCreated',
            field=models.DateField(default=datetime.date.today, editable=False),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='serialNumber',
            field=models.TextField(max_length=10, unique=True),
        ),
    ]
