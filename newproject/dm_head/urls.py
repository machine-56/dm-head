from django.urls import path
from . import views

urlpatterns = [
    path('', views.dm_home, name='dm_home'),
    path('work/', views.dm_work, name='dm_work'),

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('register-client/', views.register_client, name='register_client'),
    path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),

    path('register-work/', views.register_work, name='register_work'),

    path('check-unique/', views.check_unique_field, name='check_unique_field'),
    path('get-client/<int:client_id>/', views.get_client, name='get_client'),
    path('create-work/', views.create_work, name='create_work'),
    path('get-tasks/', views.get_available_tasks, name='get_available_tasks'),
]
