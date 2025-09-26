from .models import Notification

def create_notification(user, message, url=''):
    if user:
        Notification.objects.create(
            user=user,
            message=message,
            url=url,
        )