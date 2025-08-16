from djongo import models
from datetime import datetime

class ThreatAlert(models.Model):
    threat_id = models.AutoField(primary_key=True)
    
    # Store the image (URL-based storage)
    image_url = models.URLField(blank=True, null=True)  # Store image in cloud storage (AWS S3, Firebase, etc.)
    
    # Location details
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # Optional human-readable location
    
    # Date & Time
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto store the datetime when record is created
    
    def __str__(self):
        return f"Threat detected at {self.address or 'Unknown Location'} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
