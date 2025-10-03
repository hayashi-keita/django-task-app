from ast import Delete
from json import detect_encoding
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event
from .forms import EventForm
from datetime import datetime

class DashboardView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'schedule/dashboard.html'
    success_url = reverse_lazy('schedule:dashboard')

    def get_initial(self):
        initial = super().get_initial()
        start_datetime_str = self.request.GET.get('start_datetime')
        if start_datetime_str:
            initial['start_time'] = start_datetime_str
        return initial

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

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'schedule/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('start_time')

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'schedule/event_update.html'
    success_url = reverse_lazy('schedule:dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'schedule/event_delete.html'
    success_url = reverse_lazy('schedule:dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'schedule/event_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj