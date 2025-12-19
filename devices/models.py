from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    hostname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    os = models.CharField(max_length=100)
    os_build = models.CharField(max_length=50)
    processor = models.CharField(max_length=200)
    ram_gb = models.FloatField()

    ip_address = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=50)

    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname
