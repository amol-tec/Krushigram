from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from .serializers import SensorpropertySerializer,SensorSerializer , SensorDataSerializer,SensorpropertySerializers,SensorSerializerrr
from rest_framework import status
from rest_framework.response import Response
from .models import Sensor,Sensorproperty
from django.shortcuts import get_object_or_404
from .serializers import SensorSerializerss
from rest_framework import generics
from .serializers import SensorSerializerdd
from .models import Sensor

# Create your views here.


# class SensorDataView(APIView):
#     def post(self, request, format=None):
#         device_id = request.data.get('device_id')
#         if Sensor.objects.filter(device_id=device_id).exists():
#             return Response({'error': 'Device ID already '}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = SensorDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'succfully_Createded'},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# sensor post api
class SensorDataCreateded(GenericAPIView):
    serializer_class=SensorDataSerializer
    parser_classes=[MultiPartParser]
    def post(self, request, format=None):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
 


# sensor property post api
class Sensorpropertyview(GenericAPIView):
    serializer_class=SensorpropertySerializers
    parser_classes=[MultiPartParser]
    def post(self, request,format=None):
     
        serializer = SensorpropertySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response( {'msg':'succfully_Createded'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class SensorDataView(APIView):
#     def post(self, request, format=None):
#         device_id = request.data.get('device_id')
#         if Sensorproperty.objects.filter(device_id=device_id).exists():
#             return Response({'error': 'Device ID already '}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = SensorpropertySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'succfully_Createded'},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# sensor device list
class SensorAPIView(APIView):
    def get(self, request):
             devices = Sensor.objects.all()
             serializer = SensorSerializer(devices, many=True)
             return Response(serializer.data, status=status.HTTP_200_OK)




# device_id wise fetch data
class SensorDataView(APIView):
    def get(self,request,device_id,format=None):
        try:
            sensor_data = Sensor.objects.filter(property__device_id=device_id)
            serializer = SensorSerializer(sensor_data,many=True)
            return Response(serializer.data)
        except Sensor.DoesNotExist:
            return Response({
                'error': 'Device not found'
            }, status=404) 




        
# sensorproperty fectch data_list
class Sensorpropertyviewer(APIView):
    def get(self, request):
             devices = Sensorproperty.objects.all()
             serializer = SensorpropertySerializer(devices, many=True)
             return Response(serializer.data,status=status.HTTP_200_OK)

    


# fectch data sensor with device_id,created_at
class SensorData(APIView):
    serializer_class = SensorSerializerrr

    def get(self, request, device_id, created_at):
        sensor_data = Sensor.objects.filter(property__device_id=device_id , created_at=created_at)
        serializer = self.serializer_class(sensor_data, many=True)
        return Response(serializer.data)









# fectch data with sensor_type and created_at and device_id
class SensorListView(generics.ListAPIView):
    serializer_class = SensorSerializerdd
    queryset = Sensor.objects.all()





    
# fetch data with sensor_type and created_at

# class SensorList(APIView):
#     def get(self, request, sensor_type, created_at):
#         # Retrieve the list of Sensorproperty objects for the specified sensor_type
#         sensor_properties = Sensorproperty.objects.filter(sensor_type=sensor_type)
        
#         # Filter the Sensor objects by property and created_at for each Sensorproperty
#         sensors = []
#         # print('sensors-----',sensors)
#         for sensor_property in sensor_properties:
#             sensor_queryset = Sensor.objects.filter(property=sensor_property, 
#                                                     created_at = created_at)
#             sensors.extend(sensor_queryset)
        
#         # Check if any Sensor objects were found
#         if not sensors:
#             return Response({"message": "No Sensor data found for the specified type and date."},
#                             status=status.HTTP_404_NOT_FOUND)
        
#         # Serialize the data and return a JSON response
#         serializer = SensorSerializer(sensors, many=True)
#         return Response(serializer.data)
    


class SensorList(APIView):
    def get(self, request, sensor_type=None, created_at=None):
        # Retrieve the list of Sensorproperty objects
        sensor_properties = Sensorproperty.objects.all()
        
        # Get a list of unique sensor types
        sensor_types = set([prop.sensor_type for prop in sensor_properties])
        
        if not sensor_type:
            # Return the list of sensor types
            return Response(sensor_types)
        
        # Filter the Sensorproperty objects by sensor_type
        sensor_properties = sensor_properties.filter(sensor_type=sensor_type)
        
        # Filter the Sensor objects by property and created_at for each Sensorproperty
        sensors = []
        for sensor_property in sensor_properties:
            sensor_queryset = Sensor.objects.filter(property=sensor_property, 
                                                    created_at = created_at)
            sensors.extend(sensor_queryset)
        
        # Check if any Sensor objects were found
        if not sensors:
            return Response({"message": "No Sensor data found for the specified type and date."},
                            status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data and return a JSON response
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)
   
















