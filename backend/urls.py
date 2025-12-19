
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('devices.urls')),
    path("api/devices/", include("devices.urls")),
    path("", include("dashboard.urls")),


]
