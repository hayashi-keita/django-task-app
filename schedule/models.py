from django.db import models
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evnets')
    title = models.CharField(max_length=100, verbose_name='予定タイトル')
    start_time = models.DateTimeField(verbose_name='開始日時')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='終了日時')
    description = models.TextField(blank=True, verbose_name='説明')

    def __str__(self):
        return f'{self.title} ({self.start_time})'


