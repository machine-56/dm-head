import re
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage

from django.shortcuts import render,redirect
from django.contrib import messages
from digitalmarketing.models import *


def home(request):
    return render(request,'landingpage/home.html')

def compsignup(request):
    return render(request,'landingpage/compsignup.html')

def registerbusiness(request):
    if request.method == 'POST':
        # Fetch all form data
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        company_id = request.POST.get('company_id') or 'COMID001'  # fallback
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        location = request.POST.get('location')
        website = request.POST.get('website')
        username = request.POST.get('username')
        password = request.POST.get('password')

        login_obj = LogRegister_Details.objects.create(
    log_username=username,
    log_password=password,
    position='Admin',
    is_staff=True
)


        # Save business details
        business = BusinessRegister_Details.objects.create(
            login=login_obj,
            owner_fname=fname,
            owner_lname=lname,
            company_name=company_name,
            contact_number=contact_no,
            email=email,
            website=website,
            location=location,
            company_code=company_id,
        )

        messages.success(request, 'Business registered successfully!')
        return redirect('registerbusiness')  # or another page

    return render(request, 'landingpage/compsignup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = LogRegister_Details.objects.get(log_username=username)
        except LogRegister_Details.DoesNotExist:
            messages.error(request, "Invalid username")
            return redirect(login)

        if user.log_password != password:
            messages.error(request, "Incorrect password")
            return redirect(login)

        if not user.is_staff:
            messages.error(request, "Your account is not yet approved.")
            return redirect(login)

        # Set session based on role
        if user.position == 'Admin':
            request.session['aid'] = user.log_username
            return redirect(admin_dashboard)

        elif user.position == 'Digital_Marketing_Head':
            request.session['hid'] = user.log_username
            print("Set session hid:", request.session['hid'])

            return redirect(dmhead)  # Replace with actual URL name

        elif user.position == 'Team_Lead':
            request.session['tid'] = user.log_username
            return redirect(teamlead)  # Replace with actual URL name

        elif user.position == 'Executive':
            request.session['eid'] = user.log_username
            return redirect(executive)  # Replace with actual URL name

        elif user.position == 'Data_Manager':
            request.session['did'] = user.log_username
            return redirect(manager)  # Replace with actual URL name

        elif user.position == 'Telecaller':
            request.session['tcid'] = user.log_username
            return redirect(telecaller)  # Replace with actual URL name

        else:
            messages.error(request, "Unauthorized position.")
            return redirect('login')
    return render(request,'landingpage/login.html')

from django.http import JsonResponse


def check_email(request):
    email = request.GET.get("email", None)
    exists = BusinessRegister_Details.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})

def check_company_id(request):
    company_id = request.GET.get("company_id", None)
    exists = BusinessRegister_Details.objects.filter(company_code=company_id).exists()
    return JsonResponse({"exists": exists})

def admin_dashboard(request):
    aid = request.session.get('aid')

    if not aid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    return render(request, 'admin/admindash.html', {
        'user': user,
        'company': company
    })

def dmhead(request):
    hid = request.session.get('hid')

    if not hid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=hid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
        print("dashboard",company)
        name=EmployeeRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    
    # check if Lead task exist in DB else create
    if not Work_Task.objects.filter(task_name__iexact='Lead Collection', company__isnull=True).exists():
        Work_Task.objects.create(
            task_name='Lead Collection',
            task_description='Efficient lead collection is the cornerstone of successful business growth',
        )

    return render(request, 'dmhead/headdash.html', {
        'user': user,
        'company': company,
        'name':name
    })
    
def teamlead(request):
    aid = request.session.get('tid')

    if not aid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
        name=EmployeeRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    return render(request, 'teamlead/teamleaddash.html', {
        'user': user,
        'company': company,
        'name':name
    })

def executive(request):
    aid = request.session.get('eid')

    if not aid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
        name=EmployeeRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    return render(request, 'executive/executivedash.html', {
        'user': user,
        'company': company,
        'name':name
    })

def manager(request):
    aid = request.session.get('did')

    if not aid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
        name=EmployeeRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    return render(request, 'datamanager/managerdash.html', {
        'user': user,
        'company': company,
        'name':name
    })
    
def telecaller(request):
    aid = request.session.get('tcid')

    if not aid:
        return redirect('login')  # or appropriate login URL

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
        name=EmployeeRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None
    print("hello")
    return render(request, 'telecaller/telecallerdash.html', {
        'user': user,
        'company': company,
        'name':name
    })
    
def departments(request):
    aid = request.session.get('aid')
    if not aid:
        return redirect('login')

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        user = None
        company = None

    # Save new department (if POST)
    if request.method == 'POST':
        name = request.POST.get('dept_name')
        content = request.POST.get('dept_content')
        if name and content and company:
            DepartmentRegister_Details.objects.create(
                business=company,
                name=name,
                description=content
            )
            return redirect('departments')  # Redirect to refresh page after POST

    departments = DepartmentRegister_Details.objects.filter(business=company)
    return render(request, 'admin/departments.html', {
        'departments': departments,
        'company': company
    })

from django.shortcuts import get_object_or_404

def edit_department(request, dept_id):
    dept = get_object_or_404(DepartmentRegister_Details, id=dept_id)

    aid = request.session.get('aid')
    if not aid:
        return redirect('login')

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.get(login=user)
    except (LogRegister_Details.DoesNotExist, BusinessRegister_Details.DoesNotExist):
        return redirect('departments')

    # Ensure department belongs to the current company
    if dept.business != company:
        return redirect('departments')

    if request.method == 'POST':
        name = request.POST.get('dept_name')
        content = request.POST.get('dept_content')
        if name and content:
            dept.name = name
            dept.description = content
            dept.save()
        return redirect('departments')
        
def delete_department(request, dept_id):
    dept = get_object_or_404(DepartmentRegister_Details, id=dept_id)

    aid = request.session.get('aid')
    if not aid:
        return redirect('login')

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.get(login=user)
    except (LogRegister_Details.DoesNotExist, BusinessRegister_Details.DoesNotExist):
        return redirect('departments')

    if dept.business == company:
        dept.delete()

    return redirect('departments')

def view_designations(request):
    aid = request.session.get('aid')
    if not aid:
        return redirect('login')

    try:
        user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.filter(login=user).first()
    except LogRegister_Details.DoesNotExist:
        return redirect('login')

    departments = DepartmentRegister_Details.objects.filter(business=company)
    designations = DesignationRegister_Details.objects.filter(business=company)
    
    # For dropdown from LogRegister_Details positions
    all_positions = LogRegister_Details.ROLE_CHOICES

    pos=DesignationRegister_Details.ROLE_CHOICES

    if request.method == 'POST':
        department_id = request.POST.get('department')
        dashboard_id = request.POST.get('dashboard_id')
        designation_name = request.POST.get('designation_name')
        description = request.POST.get('description')

        if department_id and designation_name:
            dept = DepartmentRegister_Details.objects.get(id=department_id)
            DesignationRegister_Details.objects.create(
                business=company,
                department=dept,
                dashboard_id=dashboard_id,
                name=designation_name,
                description=description
            )
            return redirect('view_designations')

    return render(request, 'admin/designations.html', {
        'designations': designations,
        'departments': departments,
        'all_positions': all_positions,
        'pos':pos,
        'company':company
    })


def edit_designation(request, designation_id):
    designation = get_object_or_404(DesignationRegister_Details, id=designation_id)

    if request.method == 'POST':
        department_id = request.POST.get('department')
        designation_name = request.POST.get('designation_name')
        description = request.POST.get('description')

        department = get_object_or_404(DepartmentRegister_Details, id=department_id)

        designation.department = department
        designation.name = designation_name
        designation.description = description
        designation.save()

        return redirect('view_designations')  # Replace with your actual view name

def delete_designation(request, designation_id):
    designation = get_object_or_404(DesignationRegister_Details, id=designation_id)
    designation.delete()
    return redirect('view_designations')

def empsignup(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')

        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        company_instance = BusinessRegister_Details.objects.get(company_code=company_id)

        department_instance = get_object_or_404(DepartmentRegister_Details, id=department_id)
        designation_instance = get_object_or_404(DesignationRegister_Details, id=designation_id)

        # Create Login Entry
        login_entry = LogRegister_Details.objects.create(
            log_username=username,
            log_password=password,  
              position=designation_instance.name,
            is_staff='False'  
        )

        # Create Employee Entry
        EmployeeRegister_Details.objects.create(
            login=login_entry,
            company=company_instance,
            department=department_instance,
            designation=designation_instance,
            name=name,
            contact_number=contact_number,
            email=email,
            address_line1=address
        )

        messages.success(request, 'Employee registered successfully.')
        return redirect('login')  # Or wherever you want

    # For GET request: load departments for dropdown
    departments = DepartmentRegister_Details.objects.all()
    return render(request, 'landingpage/empsignup.html', {'departments': departments})

def ajax_load_departments(request):
    company_id = request.GET.get('company_id')
    departments = DepartmentRegister_Details.objects.filter(business__company_code=company_id)
    return JsonResponse(list(departments.values('id', 'name')), safe=False)

def ajax_load_designations(request):
    department_id = request.GET.get('department_id')
    designations = DesignationRegister_Details.objects.filter(department__id=department_id)
    return JsonResponse(list(designations.values('id', 'name')), safe=False)

def validate_email(request):
    email = request.GET.get('email', None)
    is_taken = EmployeeRegister_Details.objects.filter(email__iexact=email).exists()
    return JsonResponse({'is_taken': is_taken})

def login_requests(request):
    aid = request.session.get('aid')
    if not aid:
        return redirect('login')

    try:
        admin_user = LogRegister_Details.objects.get(log_username=aid)
        company = BusinessRegister_Details.objects.get(login=admin_user)
    except (LogRegister_Details.DoesNotExist, BusinessRegister_Details.DoesNotExist):
        messages.error(request, "Invalid admin session.")
        return redirect('login')

    # Get users under this company with is_staff=False
    employee_list = EmployeeRegister_Details.objects.filter(
        company=company,
        login__is_staff=False
    )

    return render(request, 'admin/requests.html', {
        'employee_list': employee_list,
        'company':company
    })

from django.views.decorators.http import require_POST

@require_POST
def accept_user(request, login_id):
    login_entry = get_object_or_404(LogRegister_Details, id=login_id)
    login_entry.is_staff = True
    login_entry.save()
    
    return redirect('login_requests')


@require_POST
def decline_user(request, login_id):
    login_entry = get_object_or_404(LogRegister_Details, id=login_id)
    # Also delete associated employee
    EmployeeRegister_Details.objects.filter(login=login_entry).delete()
    login_entry.delete()
    
    return redirect('login_requests')


# ======================================================== DM head ================================================================




def dm_work(request):
    user_id = request.session.get('hid')
    logged_in_user = LogRegister_Details.objects.get(log_username=user_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()


    return render(request, 'dmhead/dm_work.html',{
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
    })

def task_list(request):
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    company = BusinessRegister_Details.objects.get(id=dm_head_profile.company_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()


    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')

        if task_id:
            task = Work_Task.objects.get(id=task_id)
            task.task_name = task_name
            task.task_description = task_description
            task.save()
        else:
            if task_name and task_name.strip().lower() != 'lead collection':
                Work_Task.objects.create(
                    task_name=task_name,
                    task_description=task_description,
                    company=company
                )

        return redirect('task_list')

    tasks = Work_Task.objects.filter(models.Q(company=company) | models.Q(company__isnull=True)).order_by('id')
    context = {
        'tasks': tasks,
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
    }
    return render(request, 'dmhead/task_list.html', context)


def delete_task_main(request, task_id):
    task = Work_Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')


email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')
phone_regex = re.compile(r'^\d{10}$')
website_regex = re.compile(r'^https?:\/\/.+\..+')

def register_client(request):
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()


    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        data = request.POST

        client_name = data.get('client_name', '').strip()
        client_email_primary = data.get('client_email_primary', '').strip()
        client_email_alter = data.get('client_email_alter', '').strip()
        client_phone = data.get('client_phone', '').strip()
        client_phone_alter = data.get('client_phone_alter', '').strip()
        client_business_name = data.get('client_business_name', '').strip()
        client_business_email_primary = data.get('client_business_email_primary', '').strip()
        client_business_email_alter = data.get('client_business_email_alter', '').strip()
        client_business_website = data.get('client_business_website', '').strip()
        client_business_phone = data.get('client_business_phone', '').strip()
        client_business_phone_alter = data.get('client_business_phone_alter', '').strip()

        # === Validations ===
        errors = []
        if not email_regex.match(client_email_primary):
            errors.append('Personal email must be valid.')
        if client_email_primary == client_email_alter:
            errors.append('Personal alternate email must differ from primary.')
        if not phone_regex.match(client_phone):
            errors.append('Personal phone must be 10 digits.')
        if client_phone == client_phone_alter:
            errors.append('Personal alternate phone must differ from primary.')
        if not email_regex.match(client_business_email_primary):
            errors.append('Business email must be valid.')
        if client_business_email_primary == client_business_email_alter:
            errors.append('Business alternate email must differ from primary.')
        if not phone_regex.match(client_business_phone):
            errors.append('Business phone must be 10 digits.')
        if client_business_phone == client_business_phone_alter:
            errors.append('Business alternate phone must differ from primary.')
        if not website_regex.match(client_business_website):
            errors.append('Website must start with http:// or https://')

        # ====== Check uniqueness ======
        check_qs = ClientRegister.objects.all()
        if client_id:
            check_qs = check_qs.exclude(id=client_id)

        if check_qs.filter(client_email_primary=client_email_primary).exists():
            errors.append('Personal email already exists.')
        if check_qs.filter(client_phone=client_phone).exists():
            errors.append('Personal phone already exists.')
        if check_qs.filter(client_business_email_primary=client_business_email_primary).exists():
            errors.append('Business email already exists.')
        if check_qs.filter(client_business_phone=client_business_phone).exists():
            errors.append('Business phone already exists.')

        if errors:
            for err in errors:
                messages.error(request, err)
            return redirect('register_client')

        # === Save or update ===
        if client_id:
            client = ClientRegister.objects.get(id=client_id)
        else:
            client = ClientRegister()
        
        client.company = company
        client.company_id = dm_head_profile.company.id
        client.client_name = client_name
        client.client_email_primary = client_email_primary
        client.client_email_alter = client_email_alter
        client.client_phone = client_phone
        client.client_phone_alter = client_phone_alter
        client.client_business_name = client_business_name
        client.client_business_email_primary = client_business_email_primary
        client.client_business_email_alter = client_business_email_alter
        client.client_business_website = client_business_website
        client.client_business_phone = client_business_phone
        client.client_business_phone_alter = client_business_phone_alter

        client.client_address1 = data.get('client_address1', '').strip()
        client.client_address2 = data.get('client_address2', '').strip()
        client.client_address3 = data.get('client_address3', '').strip()
        client.client_place = data.get('client_place', '').strip()
        client.client_district = data.get('client_district', '').strip()
        client.client_state = data.get('client_state', '').strip()

        if request.FILES.get('client_profile'):
            client.client_profile = request.FILES.get('client_profile')

        client.client_business_address1 = data.get('client_business_address1', '').strip()
        client.client_business_address2 = data.get('client_business_address2', '').strip()
        client.client_business_address3 = data.get('client_business_address3', '').strip()
        client.client_business_place = data.get('i_client_business_place', '').strip()
        client.client_business_district = data.get('i_client_business_district', '').strip()
        client.client_business_state = data.get('i_client_business_state', '').strip()

        if request.FILES.get('business_logo'):
            client.business_logo = request.FILES.get('business_logo')
        if request.FILES.get('client_business_file'):
            client.client_business_file = request.FILES.get('client_business_file')

        client.more_description = data.get('more_description', '').strip()

        client.save()

        messages.success(request, 'Client saved successfully.')
        return redirect('register_client')

    clients = ClientRegister.objects.all()
    return render(request, 'dmhead/register_client.html', {
        'clients': clients,
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
    })


def delete_client(request, client_id):
    client = ClientRegister.objects.get(id=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully.')
    return redirect('register_client')


def register_work(request):
    works = WorkRegister.objects.all()
    user_id = request.session.get('hid')
    logged_in_user = LogRegister_Details.objects.get(log_username=user_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()


    work_data = []
    for work in works:
        has_lead_collection = work.clienttask_register_set.filter(task_name__icontains='Lead Collection').exists()
        work_data.append({
            'work': work,
            'has_lead_collection': has_lead_collection,
        })

    context = {
        'work_data': work_data,
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
    }
    return render(request, 'dmhead/register_work.html', context)


from django.http import JsonResponse
from .models import ClientRegister

def check_unique_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    exclude_id = request.GET.get('exclude_id')

    response = {'is_unique': True}

    if field and value:
        qs = ClientRegister.objects.all()
        if exclude_id:
            qs = qs.exclude(id=exclude_id)

        field_map = {
            'client_email_primary': 'client_email_primary',
            'client_email_alter': 'client_email_alter',
            'client_phone': 'client_phone',
            'client_phone_alter': 'client_phone_alter',
            'client_business_email_primary': 'client_business_email_primary',
            'client_business_email_alter': 'client_business_email_alter',
            'client_business_phone': 'client_business_phone',
            'client_business_phone_alter': 'client_business_phone_alter',
        }

        model_field = field_map.get(field)
        if model_field:
            filter_kwargs = {model_field: value}
            if qs.filter(**filter_kwargs).exists():
                response['is_unique'] = False

    return JsonResponse(response)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_work(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        company_id = request.POST.get('company_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('work_description')
        task_ids = request.POST.getlist('task_ids[]')
        new_task_name = request.POST.get('new_task')
        work_file = request.FILES.get('work_file')

        if not client_id or not company_id:
            return JsonResponse({'success': False, 'message': 'Client or company ID missing'})

        client = ClientRegister.objects.get(id=client_id)
        company = BusinessRegister_Details.objects.get(id=company_id)

        if new_task_name:
            ClientTask_Register.objects.create(
                company=company,
                client=client,
                work=None,
                task_name=new_task_name,
                task_description='(Custom Task)'
            )

        work = WorkRegister.objects.create(
            client=client,
            company=company,
            work_description=description,
            work_create_date=start_date,
            work_end_date=end_date
        )

        if work_file:
            work.work_file = work_file
            work.save()

        for task_id in task_ids:
            try:
                task = Work_Task.objects.get(id=task_id)
                ClientTask_Register.objects.create(
                    company=company,
                    client=client,
                    work=work,
                    task_name=task.task_name,
                    task_description=task.task_description
                )
            except Work_Task.DoesNotExist:
                continue

        ClientTask_Register.objects.filter(client=client, work__isnull=True).update(work=work)

        client.work_reg_status = 1
        client.save()

        return JsonResponse({'success': True, 'message': 'Work created successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


# edit work
@csrf_exempt
@require_POST
def edit_work(request):
    try:
        work_id = request.POST.get('work_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        file = request.FILES.get('work_file')

        work = WorkRegister.objects.get(id=work_id)
        work.work_create_date = start_date
        work.work_end_date = end_date
        work.work_description = description

        if file:
            if work.work_file:
                if default_storage.exists(work.work_file.name):
                    default_storage.delete(work.work_file.name)
            work.work_file = file

        work.save()
        return JsonResponse({'success': True, 'message': 'Work updated successfully'})

    except WorkRegister.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Work not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# delete work
@csrf_exempt
@require_POST
def delete_work(request, work_id):
    try:
        work = WorkRegister.objects.get(id=work_id)
        work.delete()
        return JsonResponse({'success': True, 'message': 'Work deleted successfully'})
    except WorkRegister.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Work not found'})

# edit task
@csrf_exempt
@require_POST
def edit_task(request):
    try:
        task_id = request.POST.get('task_id')
        task_name = request.POST.get('task_name')
        description = request.POST.get('task_description')
        file = request.FILES.get('task_file')

        task = ClientTask_Register.objects.get(id=task_id)
        is_common = Work_Task.objects.filter(task_name=task.task_name, company__isnull=True).exists()

        if not is_common:
            task.task_name = task_name

        task.task_description = description

        if file:
            if task.task_file and default_storage.exists(task.task_file.name):
                default_storage.delete(task.task_file.name)
            task.task_file = file

        task.save()
        return JsonResponse({'success': True, 'message': 'Task updated successfully'})
    except ClientTask_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# delete task
@csrf_exempt
@require_POST
def delete_task(request, task_id):
    try:
        task = ClientTask_Register.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'success': True, 'message': 'Task deleted successfully'})
    except ClientTask_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'})

# add task
@csrf_exempt
@require_POST
def add_more_task(request):
    try:
        work_id = request.POST.get('work_id')
        task_type = request.POST.get('task_type')
        description = request.POST.get('task_description')
        file = request.FILES.get('task_file')

        work = WorkRegister.objects.get(id=work_id)
        client = work.client
        company = work.company

        if task_type == 'client':
            task_name = request.POST.get('task_name_client').strip()

            if ClientTask_Register.objects.filter(work=work, task_name__iexact=task_name).exists():
                return JsonResponse({'success': False, 'message': 'Client task with this name already exists.'})

        else:
            task_id = request.POST.get('task_name_company')
            task = Work_Task.objects.get(id=task_id)
            task_name = task.task_name
            description = description or task.task_description

        ClientTask_Register.objects.create(
            company=company,
            client=client,
            work=work,
            task_name=task_name,
            task_description=description,
            task_file=file if file else None
        )

        return JsonResponse({'success': True, 'message': 'Task added successfully'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# add lead category btn
@csrf_exempt
@require_POST
def add_lead_category(request):
    try:
        task_id = request.POST.get('task_id')
        collection_for = request.POST.get('collection_for', '').strip()
        description = request.POST.get('description', '').strip()
        target = request.POST.get('target') or 0
        file = request.FILES.get('file')

        if not collection_for:
            return JsonResponse({'success': False, 'message': 'Collection Head is required.'})

        task = ClientTask_Register.objects.get(id=task_id)

        LeadCategory_Register.objects.create(
            client_task=task,
            collection_for=collection_for,
            description=description,
            target=target,
            file=file if file else None,
        )

        return JsonResponse({'success': True, 'message': 'Lead category added successfully'})

    except ClientTask_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# edit lead category
@csrf_exempt
@require_POST
def edit_category(request):
    try:
        category_id = request.POST.get('category_id')
        collection_for = request.POST.get('collection_for', '').strip()
        description = request.POST.get('description', '').strip()
        target = request.POST.get('target') or 0
        file = request.FILES.get('file')

        category = LeadCategory_Register.objects.get(id=category_id)
        category.collection_for = collection_for
        category.description = description
        category.target = target

        if file:
            if category.file and default_storage.exists(category.file.name):
                default_storage.delete(category.file.name)
            category.file = file

        category.save()
        return JsonResponse({'success': True, 'message': 'Category updated successfully'})
    except LeadCategory_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Category not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# delete lead category
@csrf_exempt
@require_POST
def delete_category(request, category_id):
    try:
        category = LeadCategory_Register.objects.get(id=category_id)
        category.delete()
        return JsonResponse({'success': True, 'message': 'Category deleted successfully'})
    except LeadCategory_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Category not found'})


# edit fields
def field_page(request, work_id):
    user_id = request.session.get('hid')
    logged_in_user = LogRegister_Details.objects.get(log_username=user_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()

    try:
        work = WorkRegister.objects.get(id=work_id)
        client = work.client

        lead_task = ClientTask_Register.objects.filter(
            work=work, task_name__iexact="Lead Collection"
        ).first()

        if not lead_task:
            return HttpResponse("No 'Lead Collection' task found.", status=404)

        categories = LeadCategory_Register.objects.filter(client_task=lead_task).prefetch_related('leadfield_register_set')

        context = {
            'work': work,
            'client': client,
            'lead_task': lead_task,
            'categories': categories,
            'logged_in_user': logged_in_user,
            'user_company': user_company,
            'employee_profile': employee_profile,
        }
        return render(request, 'dmhead/field_page.html', context)
    except WorkRegister.DoesNotExist:
        return HttpResponse("Work not found", status=404)

# add field
@csrf_exempt
@require_POST
def add_field(request):
    try:
        category_id = request.POST.get('category_id')
        name = request.POST.get('field_name').strip()
        description = request.POST.get('description', '').strip()

        category = LeadCategory_Register.objects.get(id=category_id)

        if LeadField_Register.objects.filter(lead_category=category, name__iexact=name).exists():
            return JsonResponse({'success': False, 'message': 'Field already exists for this category.'})

        LeadField_Register.objects.create(
            lead_category=category,
            name=name,
            description=description
        )

        return JsonResponse({'success': True, 'message': 'Field added successfully'})
    except LeadCategory_Register.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid category'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# Js get calls
from django.http import JsonResponse, Http404

def get_client(request, client_id):
    print(f'==================what the f is this : {client_id}================================')
    try:
        client = ClientRegister.objects.get(id=client_id)
        data = {
            'client_name': client.client_name,
            'client_email_primary': client.client_email_primary,
            'client_email_alter': client.client_email_alter,
            'client_phone': client.client_phone,
            'client_phone_alter': client.client_phone_alter,
            'client_address1': client.client_address1,
            'client_address2': client.client_address2,
            'client_address3': client.client_address3,
            'client_place': client.client_place,
            'client_district': client.client_district,
            'client_state': client.client_state,
            'client_business_name': client.client_business_name,
            'client_business_email_primary': client.client_business_email_primary,
            'client_business_email_alter': client.client_business_email_alter,
            'client_business_website': client.client_business_website,
            'client_business_phone': client.client_business_phone,
            'client_business_phone_alter': client.client_business_phone_alter,
            'client_business_address1': client.client_business_address1,
            'client_business_address2': client.client_business_address2,
            'client_business_address3': client.client_business_address3,
            'i_client_business_place': client.client_business_place,
            'i_client_business_district': client.client_business_district,
            'i_client_business_state': client.client_business_state,
            'more_description': client.more_description,
            'company_id': client.company.id if client.company else 'None',

        }
        return JsonResponse(data)
    except ClientRegister.DoesNotExist:
        raise Http404("Client not found")

def get_work(request, work_id):
    try:
        work = WorkRegister.objects.get(id=work_id)
        data = {
            'id': work.id,
            'start_date': work.work_create_date.isoformat() if work.work_create_date else '',
            'end_date': work.work_end_date.isoformat() if work.work_end_date else '',
            'description': work.work_description or '',
            'work_file_url': work.work_file.url if work.work_file else '',
        }
        return JsonResponse(data)
    except WorkRegister.DoesNotExist:
        raise Http404("Work not found")

def get_task(request, task_id):
    try:
        task = ClientTask_Register.objects.get(id=task_id)
        # determine if it's a company (common) task
        is_common = Work_Task.objects.filter(task_name=task.task_name, company__isnull=True).exists()

        data = {
            'client_name': task.client.client_name if task.client else '',
            'task_name': task.task_name,
            'task_description': task.task_description,
            'task_file_url': task.task_file.url if task.task_file else '',
            'is_common': is_common,
        }   
        return JsonResponse(data)
    except ClientTask_Register.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)


from itertools import chain

def get_available_tasks(request):
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    company = dm_head_profile.company

    work_id = request.GET.get('work_id')
    all_tasks = Work_Task.objects.filter(company=company)

    if work_id:
        existing_task_names = ClientTask_Register.objects.filter(work_id=work_id).values_list('task_name', flat=True)
        all_tasks = all_tasks.exclude(task_name__in=existing_task_names)

        if not any(task.strip().lower() == "lead collection" for task in existing_task_names):
            lead_collection = Work_Task.objects.filter(company__isnull=True, task_name="Lead Collection")
            all_tasks = list(lead_collection) + list(all_tasks)
    else:
        lead_collection = Work_Task.objects.filter(company__isnull=True, task_name="Lead Collection")
        all_tasks = list(lead_collection) + list(all_tasks)

    task_list = [{'id': t.id, 'name': t.task_name, 'description': t.task_description} for t in all_tasks]
    return JsonResponse({'tasks': task_list})

def get_field(request, field_id):
    try:
        field = LeadField_Register.objects.get(id=field_id)
        category = field.category
        task = category.client_task
        client = category.client_task.client.client_name,

        return JsonResponse({
            'name': field.name,
            'description': field.description or '',
            'collection_for': category.collection_for,
            'client_name': client
        })
    except LeadField_Register.DoesNotExist:
        return JsonResponse({'error': 'Field not found'}, status=404)

    

def get_category(request, category_id):
    try:
        category = LeadCategory_Register.objects.get(id=category_id)
        task = category.client_task
        client = task.client

        data = {
            'collection_for': category.collection_for,
            'description': category.description or '',
            'target': category.target,
            'file_url': category.file.url if category.file else '',
            'client_name': client.client_name if client else 'Unknown',
            'client_business': client.client_business_name if client else '',
            'category_id': category.id,
            'task_id': task.id,
        }
        return JsonResponse(data)
    except LeadCategory_Register.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

# ======================================================== DM head ================================================================