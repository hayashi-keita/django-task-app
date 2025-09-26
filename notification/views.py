from django.shortcuts import render
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('created_at')
