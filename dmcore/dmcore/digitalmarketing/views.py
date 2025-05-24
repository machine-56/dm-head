import re
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from datetime import date                                 #!===================== new import

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
        print(f'testing =========================[DEBUGGING] from dmhead : {company}')

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
    
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    company = BusinessRegister_Details.objects.filter(login=user).first()
    name=EmployeeRegister_Details.objects.filter(login=user).first()

    logged_in_user = LogRegister_Details.objects.get(log_username=user_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()


    return render(request, 'dmhead/dm_work.html',{
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
        'user': user,
        'company': company,
        'name':name
    })

def task_list(request):

    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    company = BusinessRegister_Details.objects.filter(login=user).first()
    name=EmployeeRegister_Details.objects.filter(login=user).first()

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
        'user': user,
        'company': company,
        'name':name
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
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    employee = EmployeeRegister_Details.objects.filter(login=user).first()
    company = employee.company if employee else None

    name=EmployeeRegister_Details.objects.filter(login=user).first()
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    # company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
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

    clients = ClientRegister.objects.filter(company=company)
    context = {
        'clients': clients,
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
        'user': user,
        'company': company,
        'name':name
    }
    print(context)
    return render(request, 'dmhead/register_client.html', context)


def delete_client(request, client_id):
    client = ClientRegister.objects.get(id=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully.')
    return redirect('register_client')


def register_work(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    employee = EmployeeRegister_Details.objects.filter(login=user).first()
    company = employee.company if employee else None

    name=EmployeeRegister_Details.objects.filter(login=user).first()
    works = WorkRegister.objects.filter(company=company)
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
        'user': user,
        'company': company,
        'name':name
    }
    print(context)
    return render(request, 'dmhead/register_work.html', context)

# allocate work
def allocate_work_page(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    company = BusinessRegister_Details.objects.filter(login=user).first()
    name=EmployeeRegister_Details.objects.filter(login=user).first()
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    employee = EmployeeRegister_Details.objects.filter(login=user).first()
    company = employee.company if employee else None

    team_leads = EmployeeRegister_Details.objects.filter(
        company=company,
        designation__dashboard_id='Team_Lead'
    )

    works = WorkRegister.objects.filter(company=company).select_related('client').prefetch_related('workassign_set__team_lead')

    for work in works:
        unique_tls = {}
        for wa in work.workassign_set.all():
            if wa.team_lead.id not in unique_tls:
                unique_tls[wa.team_lead.id] = wa
        work.unique_assignments = list(unique_tls.values())

    return render(request, 'dmhead/allocate_work.html', {
        'works': works,
        'team_leads': team_leads,
        'user': user,
        'company': company,
        'name':name
    })


# team lead tasks
def teamlead_tasks(request, tl_id):
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    company = BusinessRegister_Details.objects.filter(login=user).first()
    name=EmployeeRegister_Details.objects.filter(login=user).first()
    team_lead = EmployeeRegister_Details.objects.get(id=tl_id)
    assigned_work = WorkAssign.objects.filter(team_lead=team_lead)
    return render(request, 'dmhead/teamlead_tasks.html', {
        'team_lead': team_lead,
        'assigned_works': assigned_work,
        'user': user,
        'company': company,
        'name':name
    })


# add task to executive
def assign_to_exec_page(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    employee = EmployeeRegister_Details.objects.filter(login=user).first()
    company = employee.company if employee else None

    structured_assignments = []

    work_assigns = WorkAssign.objects.filter(
        company=company,
        assign_type=1
    ).select_related('client', 'team_lead').prefetch_related('client_task')

    for assign in work_assigns:
        for task in assign.client_task.all():
            if task.task_name.strip().lower() == "lead collection":
                # Split each category into its own row
                categories = LeadCateogry_TeamAllocate.objects.filter(
                    work_assign=assign,
                    lead_category__client_task=task
                ).select_related('lead_category')

                for cat in categories:
                    structured_assignments.append({
                        "client_name": assign.client.client_name,
                        "client_profile": assign.client.client_profile.url if assign.client.client_profile else '',
                        "start_date": assign.from_date,
                        "due_date": assign.due_date,
                        "team_lead": assign.team_lead.name,
                        "team_lead_id": assign.team_lead.id,
                        "assign_id": assign.id,
                        "task_name": task.task_name,
                        "is_category": True,
                        "category_id": cat.lead_category.id,
                        "category_name": cat.lead_category.collection_for,
                    })
            else:
                structured_assignments.append({
                    "client_name": assign.client.client_name,
                    "client_profile": assign.client.client_profile.url if assign.client.client_profile else '',
                    "start_date": assign.from_date,
                    "due_date": assign.due_date,
                    "team_lead": assign.team_lead.name,
                    "team_lead_id": assign.team_lead.id,
                    "assign_id": assign.id,
                    "task_name": task.task_name,
                    "task_id": task.id,
                    "is_category": False,
                })

    return render(request, 'dmhead/assign_to_exec.html', {
        'structured_assignments': structured_assignments,
        'user': user,
        'company': company,
        'name': employee
    })



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


# assign work save
@csrf_exempt
def submit_work_allocation(request):
    if request.method == 'POST':
        try:
            work_id = request.POST.get('work_id')
            task_id = request.POST.get('task_id')
            team_lead_id = request.POST.get('team_lead')
            work_type = request.POST.get('work_type')
            from_date = request.POST.get('start_date')
            due_date = request.POST.get('due_date')
            target = request.POST.get('target')
            description = request.POST.get('description', '')
            file = request.FILES.get('file')
            criteria = request.POST.get('criteria', '').strip()

            is_instagram = bool(request.POST.get('is_instagram'))
            is_facebook = bool(request.POST.get('is_facebook'))
            is_x = bool(request.POST.get('is_x'))

            instagram_target = request.POST.get('instagram_target') or 0
            facebook_target = request.POST.get('facebook_target') or 0
            x_target = request.POST.get('x_target') or 0

            category_ids = request.POST.getlist('category')

            work = WorkRegister.objects.get(id=work_id)
            task = ClientTask_Register.objects.get(id=task_id)
            team_lead = EmployeeRegister_Details.objects.get(id=team_lead_id)
            company = work.company
            client = work.client
            assign_type = 1 if work_type == 'group' else 0

            # check existing lead collection logic (same work, same task, same type, same TL)
            if task.task_name.strip().lower() == "lead collection":
                existing = WorkAssign.objects.filter(
                    work_register_id=work_id,
                    client_task=task,
                    assign_type=assign_type,
                    team_lead=team_lead
                )
                if assign_type == 0 and existing.exists():
                    return JsonResponse({'success': False, 'message': 'Single Lead Collection already assigned to this TL.'})
                if assign_type == 1 and existing.exists():
                    return JsonResponse({'success': False, 'message': 'Group Lead Collection already assigned to this TL.'})

            work_assign = WorkAssign.objects.create(
                company=company,
                client=client,
                work_register=work,
                team_lead=team_lead,
                from_date=from_date,
                due_date=due_date,
                target=target,
                description=description,
                file=file,
                assign_type=assign_type,
                status=1,
                criteria=criteria,
                is_instagram=is_instagram,
                is_facebook=is_facebook,
                is_x=is_x,
                instagram_target=instagram_target,
                facebook_target=facebook_target,
                x_target=x_target
            )
            work_assign.client_task.add(task)

            work.work_allocate_status = 1
            work.save()

            if task.task_name.strip().lower() == "lead collection":
                for cid in category_ids:
                    category = LeadCategory_Register.objects.get(id=cid)
                    LeadCateogry_TeamAllocate.objects.create(
                        team_lead=team_lead,
                        lead_category=category,
                        work_assign=work_assign,
                        from_date=from_date,
                        due_date=due_date,
                        target=target,
                        description=description,
                        file=file,
                        status=1
                    )

            return JsonResponse({'success': True, 'message': 'Work assigned to TL'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

# add new categoried to existing work in TL view
@csrf_exempt
def add_lead_category_to_existing_assignment(request):
    if request.method == 'POST':
        try:
            assign_id = request.POST.get('assign_id')
            from_date = request.POST.get('start_date')
            due_date = request.POST.get('end_date')
            target = request.POST.get('target')
            description = request.POST.get('description', '')
            file = request.FILES.get('file')
            criteria = request.POST.get('criteria', '')
            is_instagram = bool(request.POST.get('is_instagram'))
            is_facebook = bool(request.POST.get('is_facebook'))
            is_x = bool(request.POST.get('is_x'))
            instagram_target = request.POST.get('instagram_target') or 0
            facebook_target = request.POST.get('facebook_target') or 0
            x_target = request.POST.get('x_target') or 0
            category_ids = request.POST.getlist('category')

            work_assign = WorkAssign.objects.get(id=assign_id)
            team_lead = work_assign.team_lead

            for cid in category_ids:
                category = LeadCategory_Register.objects.get(id=cid)
                LeadCateogry_TeamAllocate.objects.create(
                    team_lead=team_lead,
                    lead_category=category,
                    work_assign=work_assign,
                    from_date=from_date,
                    due_date=due_date,
                    target=target,
                    description=description,
                    file=file,
                    status=1
                )

            # Update WorkAssign shared fields
            work_assign.from_date = from_date
            work_assign.due_date = due_date
            work_assign.target = target
            work_assign.description = description
            work_assign.criteria = criteria
            work_assign.is_instagram = is_instagram
            work_assign.is_facebook = is_facebook
            work_assign.is_x = is_x
            work_assign.instagram_target = instagram_target
            work_assign.facebook_target = facebook_target
            work_assign.x_target = x_target
            if file:
                work_assign.file = file
            work_assign.save()

            return JsonResponse({'success': True, 'message': 'Category(ies) added successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


# delete category from work TL view
@csrf_exempt
def delete_lead_category(request, category_id):
    try:
        record = LeadCateogry_TeamAllocate.objects.get(id=category_id)
        record.delete()
        return JsonResponse({'success': True, 'message': 'Lead category assignment deleted.'})
    except LeadCateogry_TeamAllocate.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Record not found.'})



# delete assigned task to TL
@csrf_exempt
@require_POST
def delete_all_tasks_for_tl(request, work_id, tl_id):
    try:
        assigns = WorkAssign.objects.filter(work_register_id=work_id, team_lead_id=tl_id)
        count = assigns.count()
        assigns.delete()
        return JsonResponse({'success': True, 'message': f'{count} task(s) deleted for this Team Lead.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# update lead task in team lead view
@csrf_exempt
@require_POST
def update_lead_category(request):
    try:
        lead_alloc = LeadCateogry_TeamAllocate.objects.get(id=request.POST.get('edit_id'))
        work_assign = lead_alloc.work_assign

        # Shared values
        target = request.POST.get('target')
        from_date = request.POST.get('start_date')
        due_date = request.POST.get('end_date')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        criteria = request.POST.get('criteria', '')
        is_instagram = bool(request.POST.get('is_instagram'))
        is_facebook = bool(request.POST.get('is_facebook'))
        is_x = bool(request.POST.get('is_x'))

        instagram_target = request.POST.get('instagram_target') or 0
        facebook_target = request.POST.get('facebook_target') or 0
        x_target = request.POST.get('x_target') or 0

        # Update LeadCateogry_TeamAllocate
        lead_alloc.target = target
        lead_alloc.from_date = from_date
        lead_alloc.due_date = due_date
        lead_alloc.description = description
        if file:
            lead_alloc.file = file
        lead_alloc.save()

        # Update WorkAssign
        work_assign.target = target
        work_assign.from_date = from_date
        work_assign.due_date = due_date
        work_assign.description = description
        work_assign.criteria = criteria
        work_assign.is_instagram = is_instagram
        work_assign.is_facebook = is_facebook
        work_assign.is_x = is_x
        work_assign.instagram_target = instagram_target
        work_assign.facebook_target = facebook_target
        work_assign.x_target = x_target
        if file:
            work_assign.file = file
        work_assign.save()

        return JsonResponse({'success': True, 'message': 'Lead category & work updated.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# delete assigned work (team lead view)
@csrf_exempt
@require_POST
def remove_task_from_assignment(request):
    try:
        import json
        data = json.loads(request.body)
        assign_id = data.get("assign_id")
        task_id = data.get("task_id")
        task_name = data.get("task_name")

        assign = WorkAssign.objects.get(id=assign_id)
        task = ClientTask_Register.objects.get(id=task_id)

        # Remove task from M2M
        assign.client_task.remove(task)

        # Delete related category assignments if "Lead Collection"
        if task_name == "lead collection":
            LeadCateogry_TeamAllocate.objects.filter(
                work_assign=assign,
                team_lead=assign.team_lead,
                lead_category__client_task=task
            ).delete()

        if assign.client_task.count() == 0:
            assign.delete()
            return JsonResponse({'success': True, 'message': 'Task and assignment fully removed.'})

        return JsonResponse({'success': True, 'message': f'Task "{task.task_name}" removed.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# save the allocations
@csrf_exempt
def assign_to_executives(request):
    if request.method == 'POST':
        try:
            task_id = request.POST.get('task_id')
            team_assign_id = request.POST.get('team_allocation_id')
            executive_id = request.POST.get('executive')
            from_date = request.POST.get('start_date')
            due_date = request.POST.get('due_date')
            target = request.POST.get('target')
            description = request.POST.get('description', '')
            file = request.FILES.get('file')
            lead_category_id = request.POST.get('lead_category')


            if not executive_id or not team_assign_id:
                return JsonResponse({'success': False, 'message': 'Missing required fields.'})

            executive = EmployeeRegister_Details.objects.get(id=executive_id)
            team_assign = WorkAssign.objects.get(id=team_assign_id)
            task = None

            if task_id:
                task = ClientTask_Register.objects.get(id=task_id)

            elif lead_category_id:
                category = LeadCategory_Register.objects.get(id=lead_category_id)
                task = category.client_task  # infer from category

            if not task:
                return JsonResponse({'success': False, 'message': 'Unable to resolve task.'})

            # === Create TaskAssign ===
            task_assign = TaskAssign.objects.create(
                work_assign=team_assign,
                executive=executive,
                client_task=task,
                description=description,
                file=file,
                allocate_date=from_date,
                start_date=from_date,
                due_date=due_date,
                target=target,
                status=1
            )

            # === If Lead Category: Create LeadCategory_Assign too ===
            if lead_category_id:
                team_category = LeadCateogry_TeamAllocate.objects.filter(
                    work_assign=team_assign,
                    lead_category_id=lead_category_id
                ).first()

                if not team_category:
                    return JsonResponse({'success': False, 'message': 'Category assignment to TL not found.'})

                LeadCategory_Assign.objects.create(
                    executive=executive,
                    team_allocation=team_category,
                    task_assign=task_assign,
                    description=description,
                    from_date=from_date,
                    due_date=due_date,
                    target=target,
                    file=file,
                    status=1
                )

            return JsonResponse({'success': True, 'message': 'Task assigned to executive successfully.'})

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
    
# getting task for allocation
def get_tasks_for_work(request, work_id):
    try:
        tasks = ClientTask_Register.objects.filter(work_id=work_id)
        task_list = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'name': task.task_name,
                'description': task.task_description or '',
                'is_lead_collection': task.task_name.lower() == 'lead collection'
            }
            if task_data['is_lead_collection']:
                categories = LeadCategory_Register.objects.filter(client_task=task)
                task_data['categories'] = [{'id': cat.id, 'name': cat.collection_for} for cat in categories]
            task_list.append(task_data)
        return JsonResponse({'success': True, 'tasks': task_list})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# lead categoried in team leader page
def get_lead_categories_for_task(request, assign_id):
    try:
        # Get the current assignment and work ID
        assign = WorkAssign.objects.get(id=assign_id)
        work_id = assign.work_register.id

        # Get the ClientTask with the name 'Lead Collection' for this work
        client_task = ClientTask_Register.objects.filter(
            work_id=work_id,
            task_name__iexact="lead collection"
        ).first()

        if not client_task:
            return JsonResponse({'success': False, 'categories': [], 'message': 'No Lead Collection task found for this work.'})

        # All categories for the matched task
        all_categories = LeadCategory_Register.objects.filter(client_task=client_task)

        # Categories already assigned to any TL in this work
        assigned_ids = LeadCateogry_TeamAllocate.objects.filter(
            work_assign_id=assign_id
        ).values_list('lead_category_id', flat=True)

        # Filter out already assigned categories
        available = all_categories.exclude(id__in=assigned_ids)

        data = [{'id': cat.id, 'name': cat.collection_for} for cat in available]
        return JsonResponse({'success': True, 'categories': data})

    except Exception as e:
        return JsonResponse({'success': False, 'categories': [], 'message': str(e)})

# TL name
def get_teamlead_name(request, tl_id):
    try:
        tl = EmployeeRegister_Details.objects.get(id=tl_id)
        return JsonResponse({'success': True, 'name': tl.name})
    except EmployeeRegister_Details.DoesNotExist:
        return JsonResponse({'success': False, 'name': 'Team Lead'})

# to get TL's executives
def get_employees_for_tl(request, tl_id):
    employees = AllocationDetails.objects.filter(team_lead_id=tl_id).select_related('employee')
    data = [
        {'id': emp.employee.id, 'name': emp.employee.name}
        for emp in employees if emp.employee.designation and emp.employee.designation.dashboard_id == 'Executive'
    ]
    return JsonResponse(data, safe=False)

def get_lead_categories_for_tl_task(request, assign_id):
    try:
        categories = LeadCateogry_TeamAllocate.objects.filter(
            work_assign_id=assign_id
        ).select_related('lead_category')

        data = [{'id': c.lead_category.id, 'name': c.lead_category.collection_for} for c in categories]
        return JsonResponse({'success': True, 'categories': data})
    except:
        return JsonResponse({'success': False, 'categories': []})

# new add 17 may

def get_lead_team_alloc_desc(request, category_id, assign_id):
    try:
        record = LeadCateogry_TeamAllocate.objects.get(
            lead_category_id=category_id,
            work_assign_id=assign_id
        )
        return JsonResponse({
            'description': record.description or '',
            'file_url': record.file.url if record.file else ''
        })
    except LeadCateogry_TeamAllocate.DoesNotExist:
        return JsonResponse({'description': '', 'file_url': ''})
    except Exception as e:
        return JsonResponse({'description': '', 'file_url': ''})

def get_workassign_desc(request, assign_id):
    try:
        assign = WorkAssign.objects.get(id=assign_id)
        return JsonResponse({
            'description': assign.description or '',
            'file_url': assign.file.url if assign.file else ''
        })
    except WorkAssign.DoesNotExist:
        return JsonResponse({'description': '', 'file_url': ''})
    except Exception as e:
        return JsonResponse({'description': '', 'file_url': ''})

@csrf_exempt
def get_full_workassign(request, assign_id):
    try:
        assign = WorkAssign.objects.get(id=assign_id)
        return JsonResponse({
            'description': assign.description or '',
            'criteria': assign.criteria or '',
            'file_url': assign.file.url if assign.file else '',
            'is_instagram': assign.is_instagram,
            'instagram_target': assign.instagram_target,
            'is_facebook': assign.is_facebook,
            'facebook_target': assign.facebook_target,
            'is_x': assign.is_x,
            'x_target': assign.x_target,
        })
    except WorkAssign.DoesNotExist:
        return JsonResponse({'error': 'WorkAssign not found'}, status=404)


# ======================================================== DM head ================================================================


# ======================================================== teamlead ================================================================
def teamlead_work(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('tid'))
    name = EmployeeRegister_Details.objects.filter(login=user).first()
    company = name.company if name else None

    context={
        'user': user,
        'company': company,
        'name': name,
    }
    return render(request, 'teamlead/tl_works.html', context)


def individual_work_main(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('tid'))
    name = EmployeeRegister_Details.objects.filter(login=user).first()
    company = name.company if name else None

    context={
        'user': user,
        'company': company,
        'name': name,
    }
    print(context)
    return render(request, 'teamlead/individual_work_main.html', context)


@csrf_exempt
def tl_new_works(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('tid'))
    name = EmployeeRegister_Details.objects.filter(login=user).first()
    company = name.company if name else None

    # Accept logic
    if request.method == 'POST':
        task_type = request.POST.get('type')
        object_id = request.POST.get('id')
        try:
            if task_type == 'normal':
                task = WorkAssign.objects.get(id=object_id)
                task.status = 2
                task.accept_date = date.today()
                task.save()
                print(f"[DEBUG] Accepted WorkAssign {object_id}")  #!========delete this line =============

            elif task_type == 'lead_collection':
                record = LeadCateogry_TeamAllocate.objects.get(id=object_id)
                record.status = 2
                record.accept_date = date.today()
                record.save()
                print(f"[DEBUG] Accepted LeadCateogry_TeamAllocate {object_id}")  #!========delete this line =============

        except Exception as e:
            print(f"[ERROR] Accept failed: {e}")  #!========delete this line =============
            
    # GET logic (same as now)
    all_data = []

    work_assigns = WorkAssign.objects.filter(team_lead=name, status=1).select_related('client')
    print(f'[DEBUG]================={name}=======================================')
    for assign in work_assigns:
        for task in assign.client_task.all():
            if task.task_name.strip().lower() != "lead collection":
                all_data.append({
                    'type': 'normal',
                    'assign_id': assign.id,
                    'task_id': task.id,
                    'task_name': task.task_name,
                    'task_description': assign.description or '',
                    'start_date': assign.from_date,
                    'end_date': assign.due_date,
                    'assign_date': assign.assign_date,
                    'accept_date': assign.accept_date,
                    'client_name': assign.client.client_name if assign.client else '',
                    'target': assign.target,
                    'file_url': assign.file.url if assign.file else ''
                })

    lead_tasks = LeadCateogry_TeamAllocate.objects.filter(team_lead=name, status=1).select_related('lead_category', 'work_assign__client')
    for record in lead_tasks:
        lead = record.lead_category
        assign = record.work_assign
        all_data.append({
            'type': 'lead_collection',
            'team_alloc_id': record.id,
            'assign_id': assign.id,
            'task_id': lead.id,
            'task_name': lead.collection_for or 'Lead Collection',
            'task_description': record.description or '',
            'start_date': record.from_date,
            'end_date': record.due_date,
            'assign_date': assign.assign_date,
            'client_name': assign.client.client_name if assign.client else '',
            'accept_date': record.accept_date,
            'target': record.target,
            'file_url': record.file.url if record.file else ''
        })

    context = {
        'user': user,
        'company': company,
        'name': name,
        'new_works': all_data,
    }

    return render(request, 'teamlead/tl_new_works.html', context)

def tl_ongoing_works(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('tid'))
    name = EmployeeRegister_Details.objects.filter(login=user).first()
    company = name.company if name else None

    #* ======================== POST: Save Daily Work Report =======================
    if request.method == 'POST':
        print("[POST DATA]", request.POST)  #!========delete this line =============

        try:
            task_assign_id = request.POST.get('task_assign_id')
            title = request.POST.get('title')
            description = request.POST.get('work_description')
            achieved = int(request.POST.get('achieved') or 0)
            uploaded_file = request.FILES.get('work_file')

            task_assign = TaskAssign.objects.get(id=task_assign_id)
            target = task_assign.target


            # Save daily task
            task_detail = TaskDetails(
                task_assign=task_assign,
                title=title,
                description=description,
                target=target,
                status=0,
                achieved_target=achieved
            )

            if uploaded_file:
                task_detail.file = uploaded_file

            task_detail.save()

            messages.success(request, "Daily report added successfully.")
            print(f"[DEBUG] Daily work saved for TaskAssign ID {task_assign_id}")  #!========delete this line =============
            return redirect('tl_ongoing_works')

        except Exception as e:
            messages.error(request, "Failed to submit daily report.")
            print(f"[ERROR] Failed to save daily work: {e}")  #!========delete this line =============
            return redirect('tl_ongoing_works')


    #* ======================== GET: Render Ongoing Works ==========================
    all_data = []

    work_assigns = WorkAssign.objects.filter(team_lead=name, status=2).select_related('client')
    print(f'[DEBUG]=============================TL name : {name}========================================')
    for assign in work_assigns:
        for task in assign.client_task.all():
            if task.task_name.strip().lower() != "lead collection":
                task_assign = TaskAssign.objects.filter(work_assign=assign, client_task=task).first()
                if not task_assign:
                    continue  # skip if no matching TaskAssign

                progress = 0
                try:
                    progress = int((assign.target_achieved / assign.target) * 100) if assign.target else 0
                except:
                    pass

                all_data.append({
                    'type': 'normal',
                    'assign_id': assign.id,
                    'task_assign_id': task_assign.id,
                    'task_id': task.id,
                    'task_name': task.task_name,
                    'task_description': assign.description or '',
                    'start_date': assign.from_date,
                    'end_date': assign.due_date,
                    'assign_date': assign.assign_date,
                    'accept_date': assign.accept_date,
                    'client_name': assign.client.client_name if assign.client else '',
                    'target': assign.target,
                    'achieved': assign.target_achieved,
                    'file_url': assign.file.url if assign.file else '',
                    'progress': progress,
                })

    lead_tasks = LeadCateogry_TeamAllocate.objects.filter(team_lead=name, status=2).select_related('lead_category', 'work_assign__client')
    for record in lead_tasks:
        lead = record.lead_category
        assign = record.work_assign
        task_assign = TaskAssign.objects.filter(
            work_assign=assign,
            client_task__task_name__iexact='lead collection'
        ).first()

        progress = 0
        try:
            progress = int((record.target_achieved / record.target) * 100) if record.target else 0
        except:
            pass

        all_data.append({
            'type': 'lead_collection',
            'team_alloc_id': record.id,
            'assign_id': assign.id,
            'task_assign_id': task_assign.id,
            'task_id': lead.id,
            'task_name': lead.collection_for or 'Lead Collection',
            'task_description': record.description or '',
            'start_date': record.from_date,
            'end_date': record.due_date,
            'assign_date': assign.assign_date,
            'accept_date': record.accept_date,
            'client_name': assign.client.client_name if assign.client else '',
            'target': record.target,
            'achieved': record.target_achieved,
            'file_url': record.file.url if record.file else '',
            'progress': progress,
        })

    context = {
        'user': user,
        'company': company,
        'name': name,
        'ongoing_works': all_data,
        'today': date.today(),
    }

    print(f"[DEBUG] Ongoing Works Count for TL {name.name}: {len(all_data)}")  #!========delete this line =============
    return render(request, 'teamlead/tl_ongoing_works.html', context)




def tl_daily_work_leads(request, team_alloc_id): 

    if request.method == 'POST':
        try:
            task_assign_id = request.POST.get('task_assign_id')
            title = request.POST.get('title')
            description = request.POST.get('work_description')
            achieved = int(request.POST.get('achieved') or 0)
            uploaded_file = request.FILES.get('work_file')

            task_assign = get_object_or_404(TaskAssign, id=task_assign_id)
            target = task_assign.target

            # Save daily task
            task_detail = TaskDetails(
                task_assign=task_assign,
                title=title,
                description=description,
                target=target,
                status=0,
                achieved_target=achieved,
                verified_target=0
            )

            if uploaded_file:
                task_detail.file = uploaded_file

            task_detail.save()
            messages.success(request, "Lead Collection daily work added successfully.")
            print(f"[DEBUG] Saved daily work for TaskAssign ID {task_assign_id}")  #!========delete this line =============
            return redirect('tl_daily_work_leads', team_alloc_id=team_alloc_id)

        except Exception as e:
            messages.error(request, "Failed to save daily work.")
            print(f"[ERROR] Failed to save daily work: {e}")  #!========delete this line =============
            return redirect('tl_daily_work_leads', team_alloc_id=team_alloc_id)

    # *=================== page rendering logic ==========================
    team_alloc = LeadCateogry_TeamAllocate.objects.select_related(
        'lead_category', 'work_assign__client'
    ).filter(id=team_alloc_id).first()

    if not team_alloc:
        messages.error(request, "Invalid team allocation ID.")
        return redirect('tl_ongoing_works')

    client = team_alloc.work_assign.client
    lead_category = team_alloc.lead_category

    # Fetch custom fields
    custom_fields = LeadField_Register.objects.filter(
        lead_category=lead_category
    ).values_list('name', flat=True)


    task_assign = TaskAssign.objects.filter(
        work_assign=team_alloc.work_assign,
        client_task__task_name__iexact='lead collection'
    ).first()

    progress = task_assign.progress

    context = {
        'today': date.today(),
        'clients': [{
            'client_name': client.client_name,
            'from_date': team_alloc.from_date,
            'due_date': team_alloc.due_date,
            'progress': progress,
            'required_fields': list(custom_fields)
        }],
        'team_alloc_id': team_alloc.id,
        'lead_category_name': lead_category.collection_for,
        'task_name': 'Lead Collection',
        'task_assign_id': task_assign.id,
    }

    return render(request, 'teamlead/tl_lead_daily_table.html', context)


def tl_view_daily_work(request, task_assign_id):
    task = TaskAssign.objects.filter(id=task_assign_id).first()
    if not task:
        messages.error(request, "Invalid TaskAssign ID.")
        return redirect('tl_ongoing_works')

    reports = TaskDetails.objects.filter(task_assign=task)

    context = {
        'task': task,
        'reports': reports,
    }
    return render(request, 'teamlead/tl_view_daily_work.html', context)


# completed page render
def tl_completed_works(request):
    user = LogRegister_Details.objects.get(log_username=request.session.get('tid'))
    name = EmployeeRegister_Details.objects.filter(login=user).first()

    all_data = []

    work_assigns = WorkAssign.objects.filter(team_lead=name, status=3).select_related('client')
    for assign in work_assigns:
        for task in assign.client_task.all():
            if task.task_name.strip().lower() != "lead collection":
                task_assign = TaskAssign.objects.filter(work_assign=assign, client_task=task).first()
                if not task_assign:
                    continue

                progress = task_assign.progress if hasattr(task_assign, 'progress') else 0

                all_data.append({
                    'task_name': task.task_name,
                    'start_date': assign.from_date,
                    'end_date': assign.due_date,
                    'accept_date': assign.accept_date,
                    'task_assign_id': task_assign.id,
                    'progress': progress,
                })

    context = {
        'completed_tasks': all_data
    }

    return render(request, 'teamlead/tl_completed_works.html', context)


# fetch data from db
@csrf_exempt
def tl_get_data_workassign(request):
    tl_id = request.GET.get('id')
    status = request.GET.get('status')

    print(f"[DEBUG] WorkAssign fetch for TL: {tl_id} with status: {status}")  #!========delete this line =============

    try:
        data = []
        records = WorkAssign.objects.filter(team_lead_id=tl_id, status=status).select_related('client', 'team_lead')
        for rec in records:
            for task in rec.client_task.all():
                if task.task_name.strip().lower() != 'lead collection':
                    data.append({
                        'type': 'normal',
                        'assign_id': rec.id,
                        'task_id': task.id,
                        'task_name': task.task_name,
                        'task_description': task.task_description,
                        'start_date': rec.from_date,
                        'end_date': rec.due_date,
                        'assign_date': rec.assign_date,
                        'accept_date': rec.accept_date,
                        'client_name': rec.client.client_name if rec.client else '',
                        'target': rec.target,
                        'file_url': rec.file.url if rec.file else '',
                    })
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        print(f"[ERROR] tl_get_data_workassign failed: {e}")  #!========delete this line =============
        return JsonResponse({'success': False, 'message': str(e)})
    

@csrf_exempt
def tl_get_data_leadcateogry_teamallocate(request):
    tl_id = request.GET.get('id')
    status = request.GET.get('status')

    print(f"[DEBUG] LeadCateogry_TeamAllocate fetch for TL: {tl_id} with status: {status}")  #!========delete this line =============

    try:
        data = []
        records = LeadCateogry_TeamAllocate.objects.filter(team_lead_id=tl_id, status=status).select_related('lead_category', 'work_assign__client')
        for rec in records:
            lead = rec.lead_category
            data.append({
                'type': 'lead_collection',
                'assign_id': rec.work_assign.id,
                'category_id': lead.id,
                'task_name': 'Lead Collection',
                'task_description': lead.description,
                'start_date': rec.from_date,
                'end_date': rec.due_date,
                'assign_date': rec.work_assign.assign_date,
                'accept_date': rec.work_assign.accept_date,
                'client_name': rec.work_assign.client.client_name if rec.work_assign.client else '',
                'target': rec.target,
                'file_url': rec.file.url if rec.file else '',
                'team_alloc_id': rec.id,
            })
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        print(f"[ERROR] tl_get_data_leadcateogry_teamallocate failed: {e}")  #!========delete this line =============
        return JsonResponse({'success': False, 'message': str(e)})

# ======================================================== teamlead ================================================================