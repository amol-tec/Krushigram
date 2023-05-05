from django.db import models
from datetime import datetime

# Create your models here.



class Sensorproperty(models.Model):
    SOIL_SENSOR = 'Soil sensor'
    WEATHER_SENSOR = 'Weather sensor'
    SENSOR_CHOICES = (
        (SOIL_SENSOR, 'Soil Sensor'),
        (WEATHER_SENSOR, 'Weather Sensor'),
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    device_id = models.CharField(max_length=255)
    sensor_type = models.CharField(max_length=255, choices=SENSOR_CHOICES)





class Sensor(models.Model):
    # device_id = models.CharField(max_length=255)
    Battery = models.FloatField()
    EC_S1 = models.FloatField()
    EC_S2 = models.FloatField()
    Moisture_S1_P = models.FloatField()
    Moisture_S2_P = models.FloatField()
    Temperature_S1_P = models.FloatField()
    Temperature_S2_P = models.FloatField()
    property = models.ForeignKey(Sensorproperty,on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)





class Advisory(models.Model):
    crop_name = models.CharField(max_length=100 , blank= True , null = True)
    Stage = models.CharField(max_length=100 , blank = True , null = True )
    Agromet_Advisory = models.TextField(blank= True , null= True)
    created_at = models.DateField(auto_now=True,blank= True , null= True)


# from django.db import models

# class Advisory(models.Model):
#     crop_name = models.CharField(max_length=100)
#     stage_name = models.CharField(max_length=100)
#     Agromet_advisory = models.TextField()

    # def __str__(self):
    #     return f"{self.crop_name} - {self.stage_name}"


    # class Sensorproperty(models.Model):
    #     latitude =models.FloatField()
    #     longitude=models.FloatField()












    





