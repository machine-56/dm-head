# Generated by Django 5.1.6 on 2025-05-13 06:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalmarketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=255, null=True)),
                ('client_email_primary', models.EmailField(blank=True, max_length=254, null=True)),
                ('client_email_alter', models.EmailField(blank=True, max_length=254, null=True)),
                ('client_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('client_phone_alter', models.CharField(blank=True, max_length=20, null=True)),
                ('client_address1', models.CharField(blank=True, max_length=255, null=True)),
                ('client_address2', models.CharField(blank=True, max_length=255, null=True)),
                ('client_address3', models.CharField(blank=True, max_length=255, null=True)),
                ('client_place', models.CharField(blank=True, max_length=255, null=True)),
                ('client_district', models.CharField(blank=True, max_length=255, null=True)),
                ('client_state', models.CharField(blank=True, max_length=255, null=True)),
                ('client_profile', models.ImageField(blank=True, null=True, upload_to='client/profile/')),
                ('client_business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_email_primary', models.EmailField(blank=True, max_length=254, null=True)),
                ('client_business_email_alter', models.EmailField(blank=True, max_length=254, null=True)),
                ('client_business_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('client_business_phone_alter', models.CharField(blank=True, max_length=20, null=True)),
                ('client_business_website', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_address1', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_address2', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_address3', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_place', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_district', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_state', models.CharField(blank=True, max_length=255, null=True)),
                ('client_business_file', models.ImageField(blank=True, null=True, upload_to='client/files/')),
                ('business_logo', models.ImageField(blank=True, null=True, upload_to='client/logo/')),
                ('more_description', models.TextField(blank=True, null=True)),
                ('client_add_time', models.TimeField(auto_now_add=True)),
                ('client_status', models.IntegerField(default=0)),
                ('work_reg_status', models.IntegerField(default=0)),
                ('client_reg_date', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.businessregister_details')),
            ],
        ),
        migrations.CreateModel(
            name='ClientTask_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('task_description', models.TextField(blank=True, null=True)),
                ('task_file', models.FileField(blank=True, null=True, upload_to='work/task/files/')),
                ('task_allocate_status', models.IntegerField(default=0)),
                ('task_total_progress', models.IntegerField(default=0)),
                ('task_status', models.IntegerField(default=0)),
                ('task_create_date', models.DateField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.clientregister')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.businessregister_details')),
            ],
        ),
        migrations.CreateModel(
            name='LeadCategory_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_date', models.DateField(auto_now=True, null=True)),
                ('collection_for', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('target', models.IntegerField(default=0)),
                ('target_achieved', models.IntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to='work/files/')),
                ('progress', models.IntegerField(default=0)),
                ('client_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.clienttask_register')),
            ],
        ),
        migrations.CreateModel(
            name='Work_Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('task_description', models.TextField(blank=True, null=True)),
                ('task_add_time', models.TimeField(auto_now_add=True)),
                ('task_add_date', models.DateField(auto_now=True)),
                ('task_status', models.IntegerField(default=0)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.businessregister_details')),
            ],
        ),
        migrations.CreateModel(
            name='WorkRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_description', models.TextField(blank=True, null=True)),
                ('work_file', models.FileField(blank=True, null=True, upload_to='work/files/')),
                ('work_create_time', models.TimeField(auto_now_add=True)),
                ('work_create_date', models.DateField(auto_now_add=True)),
                ('work_end_date', models.DateField(blank=True, null=True)),
                ('work_progress', models.IntegerField(default=0)),
                ('work_allocate_status', models.IntegerField(default=0)),
                ('work_status', models.IntegerField(default=0)),
                ('allocated_employees', models.ManyToManyField(related_name='works_allocated', to='digitalmarketing.employeeregister_details')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.clientregister')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.businessregister_details')),
            ],
        ),
        migrations.CreateModel(
            name='LeadField_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('add_time', models.TimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('add_date', models.DateField(auto_now=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.clientregister')),
                ('lead_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.leadcategory_register')),
                ('work', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.workregister')),
            ],
        ),
        migrations.AddField(
            model_name='clienttask_register',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalmarketing.workregister'),
        ),
    ]
