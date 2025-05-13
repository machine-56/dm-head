

# Create your models here.
from django.db import models

# Create your models here.
class LogRegister_Details(models.Model):  
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Digital_Marketing_Head', 'Digital_Marketing_Head'),
        ('Team_Lead', 'Team_Lead'),
        ('Executive', 'Executive'),
        ('Data_Manager', 'Data_Manager'),
        ('Telecaller', 'Telecaller')
    ]
    
    log_username = models.CharField(max_length=255, blank=True, null=True, default='')
    log_password = models.CharField(max_length=255, blank=True, null=True, default='')
    log_date = models.DateField(auto_now_add=True)
    log_time = models.TimeField(auto_now_add=True)
    position = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True)
    is_staff = models.BooleanField(default=False)  
    active_status = models.BooleanField(default=True)  

    def __str__(self):
        return self.log_username or "Unnamed User"
    
    
class DistributorRegister_Details(models.Model):
    login = models.ForeignKey('LogRegister_Details', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_no = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.EmailField(max_length=255, blank=True, null=True)
    agencies = models.CharField(max_length=255, blank=True, null=True, default='')
    profile = models.FileField(upload_to='profiles/', blank=True, null=True)
    file = models.FileField(upload_to='employee_files/', blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True, default='')
    address2 = models.CharField(max_length=255, blank=True, null=True, default='')
    address3 = models.CharField(max_length=255, blank=True, null=True, default='')
    pin = models.CharField(max_length=50, blank=True, null=True, default='')
    location = models.CharField(max_length=150, blank=True, null=True, default='')
    district = models.CharField(max_length=150, blank=True, null=True, default='')
    state = models.CharField(max_length=150, blank=True, null=True, default='')
    active_status = models.BooleanField(default=False)
    reg_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name or "Unnamed Distributor"
    
    
class BusinessRegister_Details(models.Model):
    login = models.ForeignKey('LogRegister_Details', on_delete=models.CASCADE, null=True, blank=True)
    distributor = models.ForeignKey('DistributorRegister_Details', on_delete=models.CASCADE, null=True, blank=True)
    owner_fname = models.CharField(max_length=255, blank=True, null=True, default='')
    owner_lname = models.CharField(max_length=255, blank=True, null=True, default='')
    company_name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_number = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.EmailField(max_length=255, blank=True, null=True)
    logo = models.FileField(upload_to='profiles/', blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True, default='')
    address_line1 = models.CharField(max_length=255, blank=True, null=True, default='')
    address_line2 = models.CharField(max_length=255, blank=True, null=True, default='')
    address_line3 = models.CharField(max_length=255, blank=True, null=True, default='')
    pin = models.CharField(max_length=50, blank=True, null=True, default='')
    location = models.CharField(max_length=150, blank=True, null=True, default='')
    district = models.CharField(max_length=150, blank=True, null=True, default='')
    state = models.CharField(max_length=150, blank=True, null=True, default='')
    active_status = models.BooleanField(default=True)
    reg_date = models.DateField(auto_now_add=True)
    company_code = models.CharField(max_length=150, default='COMID001')

    def __str__(self):
        return self.company_name or "Unnamed Business"

class DepartmentRegister_Details(models.Model):
    business = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    active_status = models.BooleanField(default=True)
    description = models.TextField(default='', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'department_register_details'

    def __str__(self):
        return self.name or "Unnamed Department"
    
class DesignationRegister_Details(models.Model):
    ROLE_CHOICES = [
        ('Digital_Marketing_Head', 'Digital_Marketing_Head'),
        ('Team_Lead', 'Team_Lead'),
        ('Executive', 'Executive'),
        ('Data_Manager', 'Data_Manager'),
        ('Telecaller', 'Telecaller')
    ]
    
    business = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(DepartmentRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    dashboard_id = models.CharField(max_length=50, choices=ROLE_CHOICES,null=True, blank=True) 
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'designation_register_details'

    def __str__(self):
        return self.name or "Unnamed Designation"
    
class EmployeeRegister_Details(models.Model):
    login = models.ForeignKey(LogRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(DepartmentRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(DesignationRegister_Details, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255, default='', null=True, blank=True)
    employee_code = models.CharField(max_length=255, default='EMP001', null=True, blank=True)
    contact_number = models.CharField(max_length=255, default='', null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles', default='')
    documents = models.FileField(upload_to='employee_files', default='')

    address_line1 = models.CharField(max_length=255, default='', null=True, blank=True)
    address_line2 = models.CharField(max_length=255, default='', null=True, blank=True)
    address_line3 = models.CharField(max_length=255, default='', null=True, blank=True)
    pin = models.CharField(max_length=50, default='', null=True, blank=True)
    location = models.CharField(max_length=150, default='', null=True, blank=True)
    district = models.CharField(max_length=150, default='', null=True, blank=True)
    state = models.CharField(max_length=150, default='', null=True, blank=True)
    STATUS_CHOICES = (
        ('Approved','Approved'),
        ('Pending','Pending'),
    )
    active_status = models.CharField(max_length=50,choices=STATUS_CHOICES,null=True,default='Pending')
    verification_status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'employee_register_details'

    def __str__(self):
        return self.name or "Unnamed Employee"
    



class EmployeeSchedule(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey('EmployeeRegister_Details', on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    schedule_head = models.CharField(max_length=255, null=True, blank=True)
    todo_content = models.TextField(null=True, blank=True)
    log_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    schedule_status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"{self.emp} - {self.schedule_head or 'Schedule'} ({self.schedule_status})"
    
    
class Feedback(models.Model):
    employee = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True, blank=True)  # Receiver of feedback
    from_id = models.IntegerField(default=0)  # ID of the person giving feedback
    from_name = models.CharField(max_length=255, null=True, blank=True)  # Name of the sender
    feedback_content = models.TextField(null=True, blank=True)  # Feedback content
    feedback_date = models.DateField(null=True, blank=True)  # Feedback date

    def __str__(self):
        return f"Feedback by {self.from_name or 'Unknown'} to {self.employee}"
    
    
class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    employee = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True, blank=True) # Employee who submitted the complaint
    compaint_head = models.CharField(max_length=255, null=True, blank=True) # Title or subject of the complaint
    compaint_content = models.TextField(null=True, blank=True)  # Detailed complaint content
    complaint_date = models.DateField(auto_now_add=True, null=True)
    action = models.TextField(null=True, blank=True) # Action taken on complaint (if any)
    action_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # Current status of the complaint

    def __str__(self):
        return f"Complaint by {self.employee} - {self.get_status_display()}"
    
    
class ActionTaken(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    employee = models.ForeignKey(EmployeeRegister_Details,on_delete=models.CASCADE,null=True,blank=True)
    from_id = models.IntegerField(default=0) # ID of the person who took the action
    from_name = models.CharField(max_length=255,null=True,blank=True) # Name of the person who took the action
    act_reason = models.TextField(null=True,blank=True) # Reason for the action
    act_head = models.CharField(max_length=255,null=True,blank=True) # Short title/headline of the action
    act_content = models.TextField(null=True,blank=True) # Detailed description of the action
    action_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Action on {self.employee} - {self.title or 'No Title'}"
    
    
class EmployeeLeave(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), 
        ('approved', 'Approved'), 
        ('rejected', 'Rejected'),
    )
    
    employee = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    leave_type = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    number_of_days = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateField(auto_now_add=True, null=True)
    status_changed_date = models.DateField(null=True, blank=True)
    request_file = models.FileField(upload_to='leave/files/', null=True, blank=True)

    def __str__(self):
        return f"Leave Request by {self.employee} ({self.start_date} to {self.end_date})"

class AllocationDetails(models.Model):
    employee = models.ForeignKey(EmployeeRegister_Details,on_delete=models.CASCADE,null=True,blank=True)  # The employee being allocated
    team_lead = models.ForeignKey(EmployeeRegister_Details,on_delete=models.CASCADE,related_name="allocated_employees",null=True,blank=True) 
    # The team lead to whom the employee is allocated
    allocate_status = models.IntegerField(default=0)
    allocation_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def _str_(self):
        return f"{self.employee} -> {self.team_lead} ({self.allocate_status})"
    



    

