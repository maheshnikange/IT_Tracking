from django.urls import path
from .views import register_device,device_heartbeat,refresh_location,device_location_view,upload_screenshot,device_list,device_screenshot_list

urlpatterns = [
    path("register/", register_device),
    path("devices/<str:device_id>/location/", device_location_view, name="device-location"),

    path("heartbeat/", device_heartbeat),
    path("refresh-location/<int:pk>/", refresh_location),


     # Device list
    path("devices/", device_list, name="device-list"),

    # Screenshot views
    path("devices/<str:device_id>/screenshots/",device_screenshot_list,name="device-screenshots"),

 # API
    path("api/devices/upload-screenshot/",upload_screenshot,name="upload-screenshot"),

]
