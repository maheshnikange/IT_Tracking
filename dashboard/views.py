from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from devices.models import Device

# -------------------------
# Device dashboard view
# -------------------------

def device_list(request):
    devices = Device.objects.all().order_by("-last_seen")
    message = request.GET.get("message", "")
    return render(request, "devices.html", {"devices": devices, "message": message})

