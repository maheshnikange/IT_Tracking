from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)

    hostname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    os = models.CharField(max_length=100)
    os_build = models.CharField(max_length=200)
    processor = models.CharField(max_length=200)
    # ram_gb = models.FloatField()

    ram_gb = models.FloatField(null=True, blank=True)
    public_ip = models.GenericIPAddressField(null=True)

    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    isp = models.CharField(max_length=200, blank=True)

    last_seen = models.DateTimeField(auto_now=True)
