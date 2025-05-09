from django.db import models
from myapp.models import BusinessRegister_Details, EmployeeRegister_Details

# Create your models here.
class Work_Task(models.Model):
    company = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_description = models.TextField(null=True, blank=True)
    task_add_time = models.TimeField(auto_now_add=True)
    task_add_date = models.DateField(auto_now=True)
    task_status = models.IntegerField(default=0)

    def __str__(self):
        return self.task_name or "Unnamed Task"
    
    
class ClientRegister(models.Model):
    company = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    # Client personal info
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_email_primary = models.EmailField(null=True, blank=True)
    client_email_alter = models.EmailField(null=True, blank=True)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    client_phone_alter = models.CharField(max_length=20, null=True, blank=True)
    client_address1 = models.CharField(max_length=255, null=True, blank=True)
    client_address2 = models.CharField(max_length=255, null=True, blank=True)
    client_address3 = models.CharField(max_length=255, null=True, blank=True)
    client_place = models.CharField(max_length=255, null=True, blank=True)
    client_district = models.CharField(max_length=255, null=True, blank=True)
    client_state = models.CharField(max_length=255, null=True, blank=True)
    client_profile = models.ImageField(upload_to='client/profile/', null=True, blank=True)

    # Business details
    client_business_name = models.CharField(max_length=255, null=True, blank=True)
    client_business_email_primary = models.EmailField(null=True, blank=True)
    client_business_email_alter = models.EmailField(null=True, blank=True)
    client_business_phone = models.CharField(max_length=20, null=True, blank=True)
    client_business_phone_alter = models.CharField(max_length=20, null=True, blank=True)
    client_business_website = models.CharField(max_length=255, null=True, blank=True)
    client_business_address1 = models.CharField(max_length=255, null=True, blank=True)
    client_business_address2 = models.CharField(max_length=255, null=True, blank=True)
    client_business_address3 = models.CharField(max_length=255, null=True, blank=True)
    client_business_place = models.CharField(max_length=255, null=True, blank=True)
    client_business_district = models.CharField(max_length=255, null=True, blank=True)
    client_business_state = models.CharField(max_length=255, null=True, blank=True)
    client_business_file = models.ImageField(upload_to='client/files/', null=True, blank=True)
    business_logo = models.ImageField(upload_to='client/logo/', null=True, blank=True)

    more_description = models.TextField(null=True, blank=True)
    client_add_time = models.TimeField(auto_now_add=True)
    client_status = models.IntegerField(default=0)
    work_reg_status = models.IntegerField(default=0)
    client_reg_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.client_name or "Unnamed Client"
    
    
class WorkRegister(models.Model):
    company = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True, blank=True)
    allocated_employees = models.ManyToManyField(EmployeeRegister_Details, related_name='works_allocated')
    work_description = models.TextField(null=True, blank=True)
    work_file = models.FileField(upload_to='work/files/', null=True, blank=True)
    work_create_time = models.TimeField(auto_now_add=True)
    work_create_date = models.DateField(auto_now_add=True)
    work_end_date = models.DateField(null=True, blank=True)
    work_progress = models.IntegerField(default=0)  # e.g., 0 to 100
    work_allocate_status = models.IntegerField(default=0)  
    work_status = models.IntegerField(default=0)  

    def __str__(self):
        return f"Work for {self.client} - {self.company}"
    
    
class ClientTask_Register(models.Model):
    company = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True, blank=True)
    work = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_description = models.TextField(null=True, blank=True)
    task_file = models.FileField(upload_to='work/task/files/', null=True, blank=True)
    task_allocate_status = models.IntegerField(default=0)
    task_total_progress = models.IntegerField(default=0)
    task_status = models.IntegerField(default=0)
    task_create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} for {self.client}"
    
    
class LeadCategory_Register(models.Model):
    client_task = models.ForeignKey(ClientTask_Register, on_delete=models.CASCADE, null=True, blank=True)
    assign_date = models.DateField(auto_now=True, null=True, blank=True)
    collection_for = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    target = models.IntegerField(default=0)
    target_achieved = models.IntegerField(default=0)
    file = models.FileField(upload_to='work/files/', null=True, blank=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.collection_for} ({self.progress}%)"
    
    
class LeadField_Register(models.Model):
    client = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True, blank=True)
    work = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True, blank=True)
    lead_category = models.ForeignKey(LeadCategory_Register, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    add_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    status = models.IntegerField(default=0)
    add_date = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name or 'Unnamed Field'}"
