from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
