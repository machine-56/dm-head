from django.urls import path
from . import views

urlpatterns = [
    path('', views.dm_home, name='dm_home'),
    path('work/', views.dm_work, name='dm_work'),

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/delete/<int:task_id>/', views.delete_task_main, name='delete_task_main'),

    path('register-client/', views.register_client, name='register_client'),
    path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),

    path('register-work/', views.register_work, name='register_work'),
    path('create-work/', views.create_work, name='create_work'),
    path('edit-work/', views.edit_work, name='edit_work'),
    path('delete-work/<int:work_id>/', views.delete_work, name='delete_work'),
    path('edit-task/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('add-more-task/', views.add_more_task, name='add_more_task'),
    path('add-lead-category/', views.add_lead_category, name='add_lead_category'),
    path('edit-category/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('fields/<int:work_id>/', views.field_page, name='field_page'),
    path('add-field/', views.add_field, name='add_field'),



    path('check-unique/', views.check_unique_field, name='check_unique_field'),
    path('get-client/<int:client_id>/', views.get_client, name='get_client'),
    path('get-work/<int:work_id>/', views.get_work, name='get_work'),
    path('get-task/<int:task_id>/', views.get_task, name='get_task'),
    path('get-category/<int:category_id>/', views.get_category, name='get_category'),
    path('get-tasks/', views.get_available_tasks, name='get_available_tasks'),
    path('get-field/<int:field_id>/', views.get_field, name='get_field'),

]
