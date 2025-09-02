from django.db import models
from django.contrib.auth.models import User

class DogImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="dog_images/")
    predicted_breed = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_breed or 'Unclassified'} - {self.user.username if self.user else 'Anonymous'}"