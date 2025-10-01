from django.shortcuts import render, get_object_or_404
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import RedirectView

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('created_at')
    
class NotificationRedirectView(LoginRequiredMixin, RedirectView):
    parmanent = False

    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, user=self.request.user, pk=self.kwargs['pk'])
        notification.is_read = True
        notification.save()
        
        return notification.url


