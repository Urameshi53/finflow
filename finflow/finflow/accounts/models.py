from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='avatars/', blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"Avatar of {self.user.username}"
