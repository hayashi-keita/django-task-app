from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from accounts.models import CustomUser
from .models import Project, Task
from notification.utils import create_notification
from .forms import ProjectForm, TaskForm, TaskInprojectForm
import json

class IndexView(TemplateView):
    template_name = 'index.html'

# プロジェクト関連
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project_list.html'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project:project_list')

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all():
            raise PermissionDenied
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索・フィルタ条件を設定
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        assigned_to = self.request.GET.get('assigned_to')
        # タスク一覧をベース
        tasks = self.object.tasks.all().order_by('sort_order')
        # タイトル検索
        if q:
            tasks = tasks.filter(title__icontains=q)
        # ステータス絞り込み
        if status and status != '':
            tasks = tasks.filter(status=status)
        # 担当者絞り込み
        if assigned_to and assigned_to != '':
            tasks = tasks.filter(assigned_to=assigned_to)
        # コンテキストに渡す
        context['tasks'] = tasks
        context['q'] = q
        context['status'] = status
        context['assigned_to'] = assigned_to
        context['users'] = CustomUser.objects.all()
        return context

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/project_update.html'
    form_class = ProjectForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all():
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('project:project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    success_url = reverse_lazy('project:project_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all():
            raise PermissionDenied
        return obj

# タスク関連
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('due_date')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('project:task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.assigned_to:
            create_notification(
                user=self.object.assigned_to,
                message=f'新しいタスクが割り当てられました：{self.object.title}',
                url=self.get_success_url(),
            )
        return response

class TaskCreateInprojectView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/task_form.html'
    form_class = TaskInprojectForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        response = super().form_valid(form)

        if self.object.assigned_to:
            create_notification(
                user=self.object.assigned_to,
                message=f'新しいタスクが割り当てられました：{self.object.title}', 
                url=self.get_success_url(),  
            )
        return response
    
    def get_success_url(self):
        return reverse('project:project_detail', kwargs={'pk': self.object.project.pk})
        

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task/task_update.html'
    form_class = TaskForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.assigned_to is None or obj.assigned_to != self.request.user:
            raise PermissionDenied
        return obj
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.assigned_to:
            create_notification(
                user=self.object.assigned_to,
                message=f'タスクが更新されました：{self.object.title}',
                url=self.get_success_url(),
            )
        return response
    
    def get_success_url(self):
        return reverse('project:project_detail', kwargs={'pk': self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.assigned_to is None or obj.assigned_to != self.request.user:
            raise PermissionDenied
        return obj
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.assigned_to:
            create_notification(
                user=self.obj.assigned_to,
                message=f'タスク「{obj.title}」が削除されました',
                url=''
            )
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('project:project_detail', kwargs={'pk': self.object.project.pk})

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/task_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.assigned_to is None or obj.assigned_to != self.request.user:
            raise PermissionDenied
        return obj

# AJAXでタスク順序更新
class TaskSortUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        for item in data:
            Task.objects.filter(pk=item['pk']).update(sort_order=item['order'])
        return JsonResponse({'status': 'ok'})

# AJAXでチェックボックス完了、未完了
class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        pk = data.get('pk')
        completed = data.get('completed', False)
        task = get_object_or_404(Task, pk=pk)
        task.completed = completed
        task.save()
        return JsonResponse({'status': 'ok'})
