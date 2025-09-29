from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='氏名')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='部署')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username