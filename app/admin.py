from django.contrib import admin
from app.models import Sensor,Sensorproperty
# Register your models here.
admin.site.register(Sensor)
admin.site.register(Sensorproperty)

# @admin.register(Sensor)
# class SensorAdmin(admin.ModelAdmin):
#     readonly_fields = ('created_at', )