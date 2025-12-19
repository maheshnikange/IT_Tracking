from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from devices.models import Device

def device_list(request):
    devices = Device.objects.all().order_by("-last_seen")
    return render(request, "dashboard/device_list.html", {"devices": devices})
