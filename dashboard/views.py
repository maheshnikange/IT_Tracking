from django.shortcuts import render
from django.http import JsonResponse

from devices.models import Device

# -------------------------
# Device dashboard view
# -------------------------

def device_list(request):
    try:
        devices = Device.objects.all().order_by("-last_seen")
        message = request.GET.get("message", "")
        return render(request, "dashboard/devices.html", {"devices": devices, "message": message})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

