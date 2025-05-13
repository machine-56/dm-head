from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # example view
     path('compsignup',views.compsignup),
    path('registerbusiness', views.registerbusiness, name='registerbusiness'),
    path('login',views.login,name='login'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-company-id/', views.check_company_id, name='check_company_id'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('dmhead',views.dmhead,),
    path('teamlead',views.teamlead),
    path('executive',views.executive),
    path('manager',views.manager),
    path('telecaller',views.telecaller),
    
    path('departments',views.departments,name='departments'),
    path('departments/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('view_designations',views.view_designations,name='view_designations'),
    path('designation/edit/<int:designation_id>/', views.edit_designation, name='edit_designation'),
    path('designation/delete/<int:designation_id>/', views.delete_designation, name='delete_designation'),
    path('empsignup',views.empsignup,name='empsignup'),
    path('ajax/load-departments/', views.ajax_load_departments, name='ajax_load_departments'),
    path('ajax/load-designations/', views.ajax_load_designations, name='ajax_load_designations'),
    path('validate-email/', views.validate_email, name='validate_email'),
    path('login_requests',views.login_requests,name='login_requests'),
    path('accept-user/<int:login_id>/', views.accept_user, name='accept_user'),
    path('decline-user/<int:login_id>/', views.decline_user, name='decline_user'),

    # ===================================================== DM head =====================================================
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

    # DM head (validations, and data fetch)
    path('check-unique/', views.check_unique_field, name='check_unique_field'),
    path('get-client/<int:client_id>/', views.get_client, name='get_client'),
    path('get-work/<int:work_id>/', views.get_work, name='get_work'),
    path('get-task/<int:task_id>/', views.get_task, name='get_task'),
    path('get-category/<int:category_id>/', views.get_category, name='get_category'),
    path('get-tasks/', views.get_available_tasks, name='get_available_tasks'),
    path('get-field/<int:field_id>/', views.get_field, name='get_field'),

    # ===================================================== end DM head =====================================================

]
