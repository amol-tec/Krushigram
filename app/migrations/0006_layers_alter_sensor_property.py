# Generated by Django 4.2 on 2023-05-12 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_advisory_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sensor',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sensor_Sensorproperty', to='app.sensorproperty'),
        ),
    ]