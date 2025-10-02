from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event
from .forms import EventForm

class DashboardView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'schedule/dashboard.html'
    success_url = reverse_lazy('schedule:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        events = Event.objects.filter(
            user=self.request.user,
            start_time__year=today.year,
            start_time__month=today.month,
        ).order_by('start_time')
        context['today'] = today
        context['events'] = events

        return context


