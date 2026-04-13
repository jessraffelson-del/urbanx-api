from django.db import models

class CityService(models.Model):
    SERVICE_TYPES = [
        ('transportation', 'Transportation'),
        ('library', 'Library'),
        ('clinic', 'Clinic'),
        ('event', 'Event'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.service_type})"