from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('notifications', views.NotificationListView.as_view(), name='notification_list'),
    path('notification/<int:pk>/redirect', views.NotificationRedirectView.as_view(), name='notification_redirect'),
]