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

    path('allocate-work/', views.allocate_work_page, name='allocate_work_page'),
    path('get-tasks-for-work/<int:work_id>/', views.get_tasks_for_work, name='get_tasks_for_work'),
    path('submit-work-allocation/', views.submit_work_allocation, name='submit_work_allocation'),
    path('add-category-to-work/', views.add_lead_category_to_existing_assignment, name='add_lead_category_to_existing_assignment'),
    path('delete-lead-category/<int:category_id>/', views.delete_lead_category, name='delete_lead_category'),
    path('delete-all-tasks-for-tl/<int:work_id>/<int:tl_id>/', views.delete_all_tasks_for_tl, name='delete_all_tasks_for_tl'),
    path('assign-to-exec/', views.assign_to_exec_page, name='assign_to_exec_page'),
    path('assign-to-executives/', views.assign_to_executives, name='assign_to_executives'),

    path('teamlead-tasks/<int:tl_id>/', views.teamlead_tasks, name='teamlead_tasks'),
    path('update-lead-category/', views.update_lead_category, name='update_lead_category'),
    path('remove-task-from-assignment/', views.remove_task_from_assignment, name='remove_task_from_assignment'),

    # DM head (validations, and data fetch)
    path('check-unique/', views.check_unique_field, name='check_unique_field'),
    path('get-client/<int:client_id>/', views.get_client, name='get_client'),
    path('get-work/<int:work_id>/', views.get_work, name='get_work'),
    path('get-task/<int:task_id>/', views.get_task, name='get_task'),
    path('get-category/<int:category_id>/', views.get_category, name='get_category'),
    path('get-tasks/', views.get_available_tasks, name='get_available_tasks'),
    path('get-field/<int:field_id>/', views.get_field, name='get_field'),
    path('get-tasks-for-work/<int:work_id>/', views.get_tasks_for_work, name='get_tasks_for_work'),
    path('get-lead-categories/<int:assign_id>/', views.get_lead_categories_for_task, name='get_lead_categories_for_task'),
    path('get-teamlead-name/<int:tl_id>/', views.get_teamlead_name, name='get_teamlead_name'),
    path('get-employees-for-tl/<int:tl_id>/', views.get_employees_for_tl, name='get_employees_for_tl'),
    path('get-lead-categories-for-tl-task/<int:assign_id>/', views.get_lead_categories_for_tl_task, name='get_lead_categories_for_tl_task'),

    path('get-lead-team-alloc-desc/<int:category_id>/<int:assign_id>/', views.get_lead_team_alloc_desc, name='get_lead_team_alloc_desc'),
    path('get-workassign-desc/<int:assign_id>/', views.get_workassign_desc, name='get_workassign_desc'),
    path('get-full-workassign/<int:assign_id>/', views.get_full_workassign, name='get_full_workassign'),

    # ===================================================== end DM head =====================================================
    
    # ===================================================== teamlead =====================================================
    path('TL/work/', views.teamlead_work, name='teamlead_work'),
    path('individual-work/', views.individual_work_main, name='individual_work_main'),
    path('tl-new-works/', views.tl_new_works, name='tl_new_works'),
    path('tl-ongoing-works/', views.tl_ongoing_works, name='tl_ongoing_works'),
    path('tl-daily-work-leads/<int:team_alloc_id>/', views.tl_daily_work_leads, name='tl_daily_work_leads'),
    
    # !new 2
    path('add-daily-work/task/<int:task_assign_id>/', views.add_daily_work_task, name='add_daily_work_task'),
    path('add-daily-work/lead/<int:team_alloc_id>/<int:category_id>/', views.add_daily_work_lead, name='add_daily_work_lead'),

    path('tl_view_daily_work/<int:task_assign_id>/', views.tl_view_daily_work, name='tl_view_daily_work'),
    path('tl-completed-works/', views.tl_completed_works, name='tl_completed_works'),
    # !new
    path('manage-leads/<int:team_alloc_id>/<int:lead_category_id>/', views.manage_leads_page, name='manage_leads_page'),
    path('add-lead/', views.add_lead_manual, name='add_lead_manual'),
    path('upload-leads/', views.upload_leads_excel, name='upload_leads_excel'),
    path('download_leads_excel/<int:lead_category_id>/<int:team_alloc_id>/', views.download_leads_excel, name='download_leads_excel'),

    
    # fetch calls
    path('tl-get-data-workassign/', views.tl_get_data_workassign, name='tl_get_data_workassign'),
    path('tl-get-data-leadcateogry-teamallocate/', views.tl_get_data_leadcateogry_teamallocate, name='tl_get_data_leadcateogry_teamallocate'),
    path('get-lead-details/<int:lead_id>/', views.get_lead_details, name='get_lead_details'),

    # ===================================================== teamlead =====================================================

]
