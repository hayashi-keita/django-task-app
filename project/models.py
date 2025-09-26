from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='プロジェクト名')
    description = models.TextField(blank=True, verbose_name='詳細')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', verbose_name='プロジェクトメンバー')
    # 作成時間を編集可能
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', '未着手'),
        ('doing', '進行中'),
        ('done', '完了'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name='タイトル')
    description = models.TextField(blank=True, verbose_name='詳細')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tasks')
    due_date = models.DateField(blank=True, null=True, verbose_name='納期')
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)     
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({ self.status})'

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)

