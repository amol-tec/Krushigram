
from rest_framework import serializers
from .models import Sensor,Sensorproperty
from rest_framework import serializers
# from .models import Sensor, Sensorproperty
from .models import Advisory, Layers



class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'



class sensorSerializer(serializers.ModelSerializer):
    class Meta:
        model =Sensor
        fields = '__all__'



class SensorpropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = Sensorproperty
        fields = '__all__'



class SensorpropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensorproperty
        fields = ('latitude', 'longitude','device_id')

class SensorExcelSerializer(serializers.ModelSerializer):
    property = SensorpropertySerializer()

    class Meta:
        model = Sensor
        fields = '__all__'




class SensorSerializerrr(serializers.ModelSerializer):
    property = SensorpropertySerializer()
    class Meta:
        model = Sensor
        fields = ['Battery', 'EC_S1', 'EC_S2', 'Moisture_S1_P', 'Moisture_S2_P', 'Temperature_S1_P', 
                  'Temperature_S2_P', 'property', 'created_at']






class SensorSerializerdd(serializers.ModelSerializer):
    property = SensorpropertySerializer()
    
    class Meta:
        model = Sensor
        fields = ('Battery', 'EC_S1', 'EC_S2', 'Moisture_S1_P', 'Moisture_S2_P', 
                  'Temperature_S1_P', 'Temperature_S2_P', 'created_at', 'property')

    def validate(self, data):
        sensor_type = self.context['request'].query_params.get('sensor_type', None)
        created_at = self.context['request'].query_params.get('created_at', None)
        device_id = self.context['request'].query_params.get('device_id', None)

        if sensor_type is not None:
            data['property__sensor_type'] = sensor_type
        if created_at is not None:
            data['created_at'] = created_at
        if device_id is not None:
            data['property__device_id'] = device_id

        return data

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**self.validated_data)



class SensorpropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensorproperty
        fields = ('latitude', 'longitude','device_id')

class SensorSerializerss(serializers.ModelSerializer):
    property = SensorpropertySerializer()
    class Meta:
        model = Sensor
        fields = ('Battery', 'EC_S1', 'EC_S2', 'Moisture_S1_P', 'Moisture_S2_P', 
                  'Temperature_S1_P', 'Temperature_S2_P', 'created_at', 'property')
        


class SensorpropertydataviewSerializer(serializers.ModelSerializer):
    model = Sensorproperty
    fields = ('latitude','longitude','device_id')

class SensordataviewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Sensor
        fields = ('Battery','EC_S1','EC_S2','Moisture_S1_P','Moisture_S2_P','Temperature_S1_P','Temperature_S2_P','created_at','property') 

        


# excel download geojson data SensorSerialize
class SensorlistSerializer(serializers.ModelSerializer):
    device_id =serializers.SerializerMethodField()
    class Meta:
        model = Sensor
        fields = ('Battery', 'EC_S1', 'EC_S2', 'Moisture_S1_P', 'Moisture_S2_P', 
                  'Temperature_S1_P', 'Temperature_S2_P', 'created_at','device_id')
    
    def get_device_id(self,obj):
        device_id = obj.property.device_id
        return device_id





# ADVISORY



class AdvisorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisory
        fields = ('crop_name', 'Stage', 'Agromet_Advisory','created_at')


class uploadExcelserializer(serializers.Serializer):
    excel_file =serializers.FileField( required=False)




class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layers
        fields = "__all__"
        





class JsonuploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)


    class Meta:
        fields = ('file',)













