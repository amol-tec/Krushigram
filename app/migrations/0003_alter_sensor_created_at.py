# Generated by Django 4.2 on 2023-04-29 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_sensorproperty_sensor_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]