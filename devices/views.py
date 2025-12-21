from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Device

# -------------------------
# API to register device
# -------------------------
@api_view(["POST"])
def register_device(request):
    try:
        device_id = request.data.get("device_id")
        if not device_id:
            return Response({"status": "error", "message": "device_id missing"}, status=400)

        device, created = Device.objects.update_or_create(
            device_id=device_id,
            defaults=request.data
        )

        return Response({"status": "success", "created": created})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)




from django.shortcuts import render, get_object_or_404
from .models import Device

def device_location_view(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    context = {
        "device": device
    }
    return render(request, "dashboard/device_location.html", context)


# -------------------------
# Heartbeat API
# -------------------------
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from devices.models import Device
import json
import requests
from datetime import datetime

def get_geo_from_ip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data.get("status") == "success":
            return {
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "city": data.get("city"),
                "country": data.get("country")
            }
    except:
        pass
    return None

@csrf_exempt
def device_heartbeat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        device_id = data.get("device_id")
        if not device_id:
            return JsonResponse({"status": "error", "message": "device_id missing"}, status=400)

        device, _ = Device.objects.get_or_create(device_id=device_id)

        # Update device info
        for field in ["hostname", "username", "os", "os_build", "processor", "ram_gb", "public_ip"]:
            setattr(device, field, data.get(field, getattr(device, field, "")))

        # Get location from public IP
        if device.public_ip:
            geo = get_geo_from_ip(device.public_ip)
            if geo:
                device.latitude = geo["latitude"]
                device.longitude = geo["longitude"]
                device.city = geo["city"]
                device.country = geo["country"]

        device.last_seen = datetime.utcnow()
        device.save()

        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
# Refresh location API
# -------------------------
def refresh_location(request, pk):
    try:
        device = Device.objects.get(pk=pk)

        if device.public_ip:
            r = requests.get(f"http://ip-api.com/json/{device.public_ip}", timeout=5)
            data = r.json()

            if data.get("status") == "success":
                device.country = data.get("country", "")
                device.region = data.get("regionName", "")
                device.city = data.get("city", "")
                device.isp = data.get("isp", "")
                device.save()
            else:
                return JsonResponse({"status": "error", "message": "Failed to fetch location"}, status=500)

        return JsonResponse({"status": "updated"})

    except Device.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Device not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


