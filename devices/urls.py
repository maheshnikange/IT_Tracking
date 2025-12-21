from django.urls import path
from .views import register_device,device_heartbeat,refresh_location,device_location_view

urlpatterns = [
    path("register/", register_device),
    path("devices/<str:device_id>/location/", device_location_view, name="device-location"),

    path("heartbeat/", device_heartbeat),
    path("refresh-location/<int:pk>/", refresh_location),
]
