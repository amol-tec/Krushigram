"""KrushiGram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static
from app.views import SensorAPIView,SensorList, SensorDataView, Sensorpropertyviewer,SensorDataView, SensorDataCreateded, Sensorpropertyview,SensorListView,DumpExcelInsertxlsx,AdvisoryList,LayerList, LayerPost,SensorData,GeosensorExcelList,GeosensorList,SensorUploadView
from app.views import SensorDataView



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name ='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('sensor/', SensorDataCreateded.as_view(), name ='Sensor_created'),
    path('sensorproperty/', Sensorpropertyview.as_view(), name='device_create'),
    path('device_list/',SensorAPIView.as_view(),name='devices_list'),

    path('sensor_listProperty/',Sensorpropertyviewer.as_view(),name='sensor_list'),
    path('sensor_data/<str:device_id>/', SensorDataView.as_view(), name='sensor-data'),
  
    path('sensor/<str:device_id>/<str:created_at>/', SensorData.as_view()),
    
    path('sensors/', SensorListView.as_view()),
    path('sensors/<str:sensor_type>/<str:start_date>/<str:end_date>/', SensorList.as_view(), name='sensor-list'),
   
    path('upload-excel/',DumpExcelInsertxlsx.as_view(), name='excel_upload'),
    
    path('advisory/<str:created_at>/', AdvisoryList.as_view()),
    path('layerlist/', LayerList.as_view()),
    path('layerpost/', LayerPost.as_view()),
    # downloadExcel_list
    path('api/sensor/<str:sensor_type>/<str:start_date>/<str:end_date>/',GeosensorExcelList.as_view(), name='sensor-list-filtered'),
    path('api/sensors_geojson/<str:sensor_type>/<str:start_date>/<str:end_date>/',GeosensorList.as_view(), name='sensor-list-filtered'),
    # path('upload-json/', UploadJSONView.as_view(), name='upload_json')
    path('upload-json/', SensorUploadView.as_view(), name='sensor-upload')
    
    

    
]
 

 
   

  
  
   
   
 





