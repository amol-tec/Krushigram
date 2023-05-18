import dataclasses
from io import BytesIO
import json
from django.shortcuts import render
from openpyxl import load_workbook
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from .serializers import SensorpropertySerializer,SensorSerializer ,SensorDataSerializer,SensorpropertySerializers,SensorSerializerrr,uploadExcelserializer,AdvisorySerializer,LayerSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Sensor,Sensorproperty
from django.shortcuts import get_object_or_404
from .serializers import SensorSerializerss
from rest_framework import generics
from .serializers import SensorSerializerdd
from rest_framework.exceptions import NotFound
from .models import Sensor,Advisory,Layers
from django.contrib.gis.geos import Point
from django.http import HttpResponse
import pandas as pd

# Create your views here.





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
        sensor_data = Sensor.objects.filter(property__device_id=device_id,created_at=created_at)
        serializer = self.serializer_class(sensor_data, many=True)
        return Response(serializer.data)
    





# fectch data with sensor_type and created_at and device_id
class SensorListView(generics.ListAPIView):
    serializer_class = SensorSerializerdd
    queryset = Sensor.objects.all()





class SensorList(APIView):
    def get(self, request, sensor_type=None, start_date=None, end_date=None):
        # Retrieve the list of Sensorproperty objects
        sensor_properties = Sensorproperty.objects.all()
        
        # Get a list of unique sensor types
        sensor_types = set([prop.sensor_type for prop in sensor_properties])
      
        
        if not sensor_type:
            # Return the list of sensor types
            return Response(sensor_types)
        
        # Filter the Sensorproperty objects by sensor_type
        sensor_properties = Sensorproperty.objects.filter(sensor_type=sensor_type)
        print(sensor_properties)
        
        # Filter the Sensor objects by property and created_at between start_date and end_date for each Sensorproperty
        sensors = []
        for sensor_property in sensor_properties:
            sensor_queryset = Sensor.objects.filter(property=sensor_property, 
                                                    created_at__range=(start_date, end_date))
            # print(sensor_queryset)
            sensors.extend(sensor_queryset)
        
        # Check if any Sensor objects were found
        if not sensors:
            return Response({"message": "No Sensor data found for the specified type and date."},
                            status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data and return a JSON response
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)
    


    


class GeosensorList(APIView):
    def get(self, request, sensor_type=None, start_date=None, end_date=None):
        # Retrieve the list of Sensorproperty objects
        sensor_properties = Sensorproperty.objects.all()
        
        # Get a list of unique sensor types
        sensor_types = set([prop.sensor_type for prop in sensor_properties])
      
        
        if not sensor_type:
            # Return the list of sensor types
            return Response(sensor_types)
        
        # Filter the Sensorproperty objects by sensor_type
        sensor_properties = Sensorproperty.objects.filter(sensor_type=sensor_type)
        
        # Filter the Sensor objects by property and created_at between start_date and end_date for each Sensorproperty
        sensors = []
        for sensor_property in sensor_properties:
            sensor_queryset = Sensor.objects.filter(property=sensor_property, 
                                                    created_at__range=(start_date, end_date))
            sensors.extend(sensor_queryset)
        
        # Check if any Sensor objects were found
        if not sensors:
            return Response({"message": "No Sensor data found for the specified type and date."},
                            status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data in GeoJSON format
        data = {
            'type': 'FeatureCollection',
            'features': []
        }
        for sensor in sensors:
            point = Point(sensor.property.longitude, sensor.property.latitude)
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [point.x, point.y]
                },
                'properties': SensorSerializer(sensor).data
            }
            data['features'].append(feature)
        
        # Return the GeoJSON response
        return Response(data)
    
    







class GeosensorExcelList(APIView):
    def get(self, request, sensor_type=None, start_date=None, end_date=None):
        # Retrieve the list of Sensorproperty objects
        sensor_properties = Sensorproperty.objects.all()
        
        # Get a list of unique sensor types
        sensor_types = set([prop.sensor_type for prop in sensor_properties])
      
        if not sensor_type:
            # Return the list of sensor types
            return Response(sensor_types)
        
        # Filter the Sensorproperty objects by sensor_type
        sensor_properties = Sensorproperty.objects.filter(sensor_type=sensor_type)
        
        # Filter the Sensor objects by property and created_at between start_date and end_date for each Sensorproperty
        sensors = []
        for sensor_property in sensor_properties:
            sensor_queryset = Sensor.objects.filter(property=sensor_property, created_at__range=(start_date, end_date))
            sensors.extend(sensor_queryset)
        
        # Check if any Sensor objects were found
        if not sensors:
            return Response({"message": "No Sensor data found for the specified type and date."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data in GeoJSON format
        data = {
            'type': 'FeatureCollection',
            'features': []
        }
        for sensor in sensors:
            point = Point(sensor.property.longitude, sensor.property.latitude)
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [point.x, point.y]
                },
                'properties': SensorSerializer(sensor).data
            }
            data['features'].append(feature)
        
        # Convert GeoJSON data to pandas DataFrame
        df = pd.json_normalize(data['features']).drop(['geometry.type'], axis=1) 
        df['geometry'] = df['geometry.coordinates'].apply(lambda coords: Point(coords[0], coords[1]))
        df.drop(['geometry.coordinates'], axis=1, inplace=True)
        
        # Rename columns
        df.rename(columns={
            "properties.Battery": "Battery",
            "properties.EC_S2": "EC_S2",
            "properties.EC_S1": "EC_S1",
            "properties.Temperature_S1_P": "Temperature_S1_P",
            "properties.Temperature_S2_P": "Temperature_S2_P",
            "properties.Moisture_S1_P":"Moisture_S1_P",
            "properties.Moisture_S2_P":"Moisture_S2_P",
            "properties.device_id":"device_id",
            "properties.created_at": "created_at"
        }, inplace=True)
        
        # Write DataFrame to Excel file
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.drop(['type'], axis=1).to_excel(writer, sheet_name='Sheet1', index=False)
        writer.book.close()  

        # Set the response content type and headers
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sensor_data.xlsx"'
        
        # Write the Excel file to the response
        output.seek(0)
        response.write(output.getvalue())
        return response


# # # # Advisory

class DumpExcelInsertxlsx(generics.GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = uploadExcelserializer
    def post(self, request, format=None):
        # try:
        if 'excel_file' not in request.FILES:
            return Response({"status": "error", "message": "No file uploaded."}, status=400)
        excel_file = request.FILES["excel_file"]

        if excel_file.size == 0 or excel_file.name.endswith(".xlsx") != True:

            return Response({"status": "error","message": "only .xlsx file is supported."},status=400)

        workbook = load_workbook(filename=excel_file)
        print('------220',workbook)
        sheet_name = workbook.sheetnames[0]
        print(sheet_name)
        worksheet = workbook[sheet_name]
        print(worksheet)
        data_list = []

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if not any(row): 
                break  
            data = Advisory(crop_name=row[0], Stage=row[1], Agromet_Advisory=row[2])
            data_list.append(data)
        # print(data_list)
        Advisory.objects.bulk_create(data_list)
        return Response({"status": "Success","message": "Successfully Uploaded."})
    








class AdvisoryList(APIView):
    def get(self, request, created_at):
        advisories = Advisory.objects.filter(created_at=created_at)
        if not advisories:
            raise NotFound(detail='No advisories found for the given created_at')
        serializer = AdvisorySerializer(advisories, many=True)
        return Response(serializer.data)


class LayerList(APIView):
    def get(self, request):
        layer_list = Layers.objects.all()
        serializer = LayerSerializer(layer_list, many=True)
        return Response(serializer.data)
    

class LayerPost(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = LayerSerializer
    def post(self, request):
        serializer = LayerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        

######################################################################

# from rest_framework.views import APIView
# from rest_framework.parsers import FileUploadParser
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Sensorproperty, Sensor

# class UploadGeoJSONView(generics.GenericAPIView):
#     parser_classes = [FileUploadParser]
#     # parser_classes = [MultiPartParser] 
#     serializer_class = uploadExcelserializer

#     def post(self, request, format=None):
#         geojson_file = request.data['file']
#         # Parse the GeoJSON file and extract relevant data
#         properties = geojson_file['features'][0]['properties']
#         coordinates = geojson_file['features'][0]['geometry']['coordinates']
        
#         # Create and save Sensorproperty object
#         sensor_property = Sensorproperty(
#             latitude=coordinates[0],
#             longitude=coordinates[1],
#             device_id=properties['device_id']
#         )
#         sensor_property.save()
        
#         # Create and save Sensor object
#         sensor = Sensor(
#             Battery=properties['Battery'],
#             EC_S1=properties['EC_S1'],
#             EC_S2=properties['EC_S2'],
#             Moisture_S1_P=properties['Moisture_S1_P'],
#             Moisture_S2_P=properties['Moisture_S2_P'],
#             Temperature_S1_P=properties['Temperature_S1_P'],
#             Temperature_S2_P=properties['Temperature_S2_P'],
#             property=sensor_property
#         )
#         sensor.save()
        
#         return Response({'message': 'Successfully uploaded GeoJSON file'}, status=status.HTTP_200_OK)

        


# class UploadGeoJSONView(generics.GenericAPIView):
#     parser_classes = [FileUploadParser]
#     serializer_class = SensorSerializer
#     sensorproperty_serializer_class = SensorpropertySerializer

#     def post(self, request, format=None):
#         geojson_file = request.data['file']
#         # Parse the GeoJSON file and extract relevant data
#         properties = geojson_file['features'][0]['properties']
#         coordinates = geojson_file['features'][0]['geometry']['coordinates']
        
#         # Create and save Sensorproperty object
#         sensorproperty_serializer = self.sensorproperty_serializer_class(data={
#             'latitude': coordinates[0],
#             'longitude': coordinates[1],
#             'device_id': properties['device_id']
#         })
#         sensorproperty_serializer.is_valid(raise_exception=True)
#         sensor_property = sensorproperty_serializer.save()
        
#         # Create and save Sensor object
#         sensor_serializer = self.serializer_class(data={
#             'Battery': properties['Battery'],
#             'EC_S1': properties['EC_S1'],
#             'EC_S2': properties['EC_S2'],
#             'Moisture_S1_P': properties['Moisture_S1_P'],
#             'Moisture_S2_P': properties['Moisture_S2_P'],
#             'Temperature_S1_P': properties['Temperature_S1_P'],
#             'Temperature_S2_P': properties['Temperature_S2_P'],
#             'property': sensor_property.id
#         })
#         sensor_serializer.is_valid(raise_exception=True)
#         sensor = sensor_serializer.save()
        
#         return Response({'message': 'Successfully uploaded GeoJSON file'}, status=status.HTTP_200_OK)

# from rest_framework import generics, parsers, status
# from rest_framework.response import Response

# from .models import Sensor, Sensorproperty



# class GeoJSONUploadView(generics.GenericAPIView):
#     parser_classes = [parsers.MultiPartParser]
#     serializer_class = GeoJSONUploadSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         geojson_file = serializer.validated_data['file']
#         # Parse the GeoJSON file and extract relevant data
#         properties = geojson_file['features'][0]['properties']
#         coordinates = geojson_file['features'][0]['geometry']['coordinates']
#         sensor_type = properties['sensor_type']

#         # Create and save Sensorproperty object
#         sensor_property = Sensorproperty(
#             latitude=coordinates[1],
#             longitude=coordinates[0],
#             device_id=properties['device_id'],
#             sensor_type=sensor_type
#         )
#         sensor_property.save()

#         # Create and save Sensor object
#         sensor = Sensor(
#             Battery=properties['Battery'],
#             EC_S1=properties['EC_S1'],
#             EC_S2=properties['EC_S2'],
#             Moisture_S1_P=properties['Moisture_S1_P'],
#             Moisture_S2_P=properties['Moisture_S2_P'],
#             Temperature_S1_P=properties['Temperature_S1_P'],
#             Temperature_S2_P=properties['Temperature_S2_P'],
#             property=sensor_property
#         )
#         sensor.save()

# #         return Response({'message': 'Successfully uploaded GeoJSON file'}, status=status.HTTP_200_OK)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser, MultiPartParser
# from .serializers import SensorpropertySerializer, SensorSerializer

# class UploadView(generics.GenericAPIView):
#     parser_classes = (MultiPartParser, JSONParser)
    
#     def post(self, request, format=None):
#         file = request.data['file']
#         data = JSONParser().parse(file)
#         properties = data['properties']
#         sensors = data['sensors']
        
#         # Serialize and save Sensorproperty objects
#         for p in properties:
#             serializer = SensorpropertySerializer(data=p)
#             if serializer.is_valid():
#                 serializer.save()
        
#         # Serialize and save Sensor objects
#         for s in sensors:
#             # Convert property field to Sensorproperty object
#             s['property'] = Sensorproperty.objects.get(device_id=s['property'])
            
#             serializer = SensorSerializer(data=s)
#             if serializer.is_valid():
#                 serializer.save()
        
#         return Response({'message': 'Upload successful'})

# views.py
# api/views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import SensorpropertySerializer, SensorSerializer
# import json
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi


# class UploadJSONView(generics.GenericAPIView):
#     parser_classes = [MultiPartParser]
#     # serializer_class = UploadjsonSerializer
#     def post(self, request):
#         json_file = request.FILES.get('file')
#         if json_file:
#             try:
#                 data = json.load(json_file)
#                 sensor_type = data.get('sensor_type')

#                 # Create Sensorproperty instance
#                 sensor_property_serializer = SensorpropertySerializer(data=data)
#                 if sensor_property_serializer.is_valid():
#                     sensor_property = sensor_property_serializer.save()
#                 else:
#                     return Response(sensor_property_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#                 # Create Sensor instances
#                 sensors = data.get('sensors', [])
#                 for sensor_data in sensors:
#                     sensor_data['property'] = sensor_property.id
#                     sensor_serializer = SensorSerializer(data=sensor_data)
#                     if sensor_serializer.is_valid():
#                         sensor_serializer.save()
#                     else:
#                         return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#                 return Response("Data saved successfully!", status=status.HTTP_201_CREATED)
#             except json.JSONDecodeError:
#                 return Response("Invalid JSON format", status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)



# from rest_framework import generics
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# from rest_framework import status
# import json

# class UploadJSONView(generics.GenericAPIView):
#     parser_classes = [MultiPartParser]
#     serializer_class = SensorpropertySerializer

#     def post(self, request):
#         json_file = request.FILES.get('file')
#         if json_file:
#             try:
#                 data = json.load(json_file)
#                 serializer = self.get_serializer(data=data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response("Data saved successfully!", status=status.HTTP_201_CREATED)
#             except json.JSONDecodeError:
#                 return Response("Invalid JSON format", status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser, MultiPartParser
# from .serializers import SensorSerializer, SensorPropertySerializer

# class SensorUploadView(generics.GenericAPIView):
#     parser_classes = (JSONParser, MultiPartParser)

#     def post(self, request, format=None):
#         file_obj = request.data['file']
#         data = JSONParser().parse(file_obj)
        
#         sensor_properties = data.get('sensor_properties', [])
#         sensors = data.get('sensors', [])

#         sensor_property_serializer = SensorPropertySerializer(data=sensor_properties, many=True)
#         if sensor_property_serializer.is_valid():
#             sensor_properties = sensor_property_serializer.save()
#         else:
#             return Response(sensor_property_serializer.errors, status=400)

#         sensor_serializer = SensorSerializer(data=sensors, many=True)
#         if sensor_serializer.is_valid():
#             sensor_serializer.save(property_id__in=[prop.id for prop in sensor_properties])
#         else:
#             return Response(sensor_serializer.errors, status=400)

#         return Response("Data uploaded successfully.", status=201)
