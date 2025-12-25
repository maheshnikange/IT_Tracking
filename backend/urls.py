
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('devices.urls')),
    path("api/devices/", include("devices.urls")),
    path("", include("dashboard.urls")),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# ssh root@64.227.156.233
# http://64.227.156.233:8000/api/devices/heartbeat/

# curl -X POST http://64.227.156.233:8000/api/devices/heartbeat/ \
# -H "Content-Type: application/json" \
# -d '{"device_id": "TEST123", "hostname": "TEST-PC", "username": "user", "os": "Windows 10", "os_build": "22631", "processor": "Intel i5", "ram_gb": 8, "public_ip": "49.43.24.115"}'
