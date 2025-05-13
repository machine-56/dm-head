
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