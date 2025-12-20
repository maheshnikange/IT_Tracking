from django.urls import path
from .views import register_device,device_heartbeat,refresh_location

urlpatterns = [
    path("register/", register_device),
    path("heartbeat/", device_heartbeat),
    path("refresh-location/<int:pk>/", refresh_location),
]
