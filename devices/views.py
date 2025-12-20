from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer

@api_view(["POST"])
def register_device(request):
    device_id = request.data.get("device_id")

    device, created = Device.objects.update_or_create(
        device_id=device_id,
        defaults=request.data
    )

    return Response({
        "status": "success",
        "created": created
    })


import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device

@csrf_exempt
def device_heartbeat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body)

    device, _ = Device.objects.get_or_create(
        device_id=data["device_id"]
    )

    for field in [
        "hostname", "username", "os", "os_build",
        "processor", "ram_gb", "public_ip"
    ]:
        setattr(device, field, data.get(field))

    device.save()
    return JsonResponse({"status": "ok"})

def refresh_location(request, pk):
    device = Device.objects.get(pk=pk)

    if device.public_ip:
        r = requests.get(f"http://ip-api.com/json/{device.public_ip}")
        data = r.json()

        if data.get("status") == "success":
            device.country = data.get("country", "")
            device.region = data.get("regionName", "")
            device.city = data.get("city", "")
            device.isp = data.get("isp", "")
            device.save()

    return JsonResponse({"status": "updated"})
