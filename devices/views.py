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
