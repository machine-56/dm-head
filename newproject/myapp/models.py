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


    
