from django.shortcuts import render
from django.http import JsonResponse

from devices.models import Device

# -------------------------
# Device dashboard view
# -------------------------

# def device_list(request):
#     try:
#         devices = Device.objects.all().order_by("-last_seen")
#         message = request.GET.get("message", "")
#         return render(request, "dashboard/devices.html", {"devices": devices, "message": message})
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)


from django.shortcuts import render, get_object_or_404
# from .models import Device, DeviceScreenshot

def device_list(request):
    devices = Device.objects.all().order_by("-last_seen")
    return render(request, "devices/device_list.html", {
        "devices": devices
    })
