from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    relevance_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} at {self.company}"