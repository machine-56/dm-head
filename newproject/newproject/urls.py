from django.contrib import admin
from django.urls import include, path,re_path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('compsignup',views.compsignup),
    path('registerbusiness', views.registerbusiness, name='registerbusiness'),
    path('login',views.login,name='login'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-company-id/', views.check_company_id, name='check_company_id'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    # path('dmhead',views.dmhead,),
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

    path('dm_head/', include('dm_head.urls')),
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)