from django.db import models

class UserQuery(models.Model):
    target_market = models.CharField(max_length=255)
    desired_role = models.CharField(max_length=255)
    specific_criteria = models.TextField()

    def __str__(self):
        return f"{self.desired_role} in {self.target_market}"
