from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework import status

class DeviceSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=50)
    ram_gb = serializers.IntegerField(required=True)
    status = serializers.CharField(max_length=20)

class HeartbeatAPIView(views.APIView):
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            # Save device data
            return Response({"status": "ok"})
        else:
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
