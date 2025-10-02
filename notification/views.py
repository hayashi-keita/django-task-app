from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.views.generic.base import RedirectView

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('created_at')

class NotificationDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return redirect('notification:notification_list')
    
class NotificationRedirectView(LoginRequiredMixin, RedirectView):
    parmanent = False

    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, user=self.request.user, pk=self.kwargs['pk'])
        notification.is_read = True
        notification.save()
        
        return notification.url

class NotificationBulkDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        pks = request.POST.getlist('selected_notifications')
        if pks:
            Notification.objects.filter(pk__in=pks, user=request.user).delete()    
        return redirect('notification:notification_list')

