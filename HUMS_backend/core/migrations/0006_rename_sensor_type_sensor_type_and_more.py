# Generated by Django 4.1.7 on 2023-04-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_type_sensor_sensor_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensor',
            old_name='sensor_type',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='sample',
            name='valueType',
            field=models.CharField(choices=[('OW', 'Water'), ('OF', 'Fuel'), ('MF', 'Ferrous'), ('MN', 'Non-Ferrous')], max_length=2),
        ),
    ]
