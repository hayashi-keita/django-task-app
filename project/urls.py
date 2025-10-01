from django.urls import path
from . import views

handler403 = 'project.views.custom_permission_denied_view'

app_name = 'project'

urlpatterns = [
    # TOPページ
    path('', views.IndexView.as_view(), name='index'),
    # プロジェクト関連
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/detail/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    # タスク関連
    path('tasks', views.TaskListView.as_view(), name='task_list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:project_pk>/create/', views.TaskCreateInprojectView.as_view(), name='task_create_in_project'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/detail/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('attachment/<int:pk>/update/', views.AttachmentUpdateView.as_view(), name='attachment_update'),
    path('attachment/<int:pk>/delete/', views.AttachmentDeleteView.as_view(), name='attachment_delete'),
    path('task/<int:pk>/attachment/', views.AttachmentCreateView.as_view(), name='attachment_create'),
    # タスクの順番替え
    path('task/sort/', views.TaskSortUpdateView.as_view(), name='task_sort'),
    path('task/toggle_complete/', views.TaskToggleCompleteView.as_view(), name='task_toggle_complete'),
    # グラフ
    path('chart/', views.ProjectAchienementChartView.as_view(), name='project_chart'),
]