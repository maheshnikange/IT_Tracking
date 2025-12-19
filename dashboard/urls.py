from django.urls import path
from .views import device_list

urlpatterns = [
    path("devices/", device_list),
]
