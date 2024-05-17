from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile-pics', default='default.jpg')
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user} profile"
