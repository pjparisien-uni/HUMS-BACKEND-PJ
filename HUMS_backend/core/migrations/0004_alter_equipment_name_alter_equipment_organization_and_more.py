# Generated by Django 4.1.7 on 2023-04-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_equipment_sensors_alter_sensor_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='organization',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='type',
            field=models.CharField(choices=[('V', 'Vehicle'), ('M', 'Marine'), ('A', 'Aerial'), ('S', 'Stationary')], max_length=1),
        ),
    ]
