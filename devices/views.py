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


# -------------------------
# Heartbeat API
# -------------------------
@csrf_exempt
def device_heartbeat(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST only"}, status=405)

        import json
        data = json.loads(request.body)

        device_id = data.get("device_id")
        if not device_id:
            return JsonResponse({"status": "error", "message": "device_id missing"}, status=400)

        device, _ = Device.objects.get_or_create(device_id=device_id)

        for field in ["hostname", "username", "os", "os_build", "processor", "ram_gb", "public_ip"]:
            setattr(device, field, data.get(field, ""))

        device.save()
        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# -------------------------
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


