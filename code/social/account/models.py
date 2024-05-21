from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to='users/%Y/%m/%d')

    def __str__(self):
        return f"Profile for {self.user.username}"
