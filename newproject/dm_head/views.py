import re
from django.shortcuts import redirect, render
from django.contrib import messages

from myapp.models import LogRegister_Details, BusinessRegister_Details, EmployeeRegister_Details
from .models import Work_Task, ClientRegister, WorkRegister, ClientTask_Register, LeadCategory_Register

from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def dm_home(request):

    user_id = request.session.get('hid')
    if not user_id:
        return redirect('login')
    
    logged_in_user = LogRegister_Details.objects.get(log_username=user_id)
    user_company = BusinessRegister_Details.objects.filter(login=logged_in_user).first()
    employee_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()

    context = {
        'logged_in_user': logged_in_user,
        'user_company': user_company,
        'employee_profile': employee_profile,
    }

    return render(request, 'dm_head/dm_home.html', context)

def dm_work(request):
    return render(request, 'dm_head/dm_work.html')

def task_list(request):
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    company = BusinessRegister_Details.objects.get(id=dm_head_profile.company_id)

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

    tasks = Work_Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'dm_head/task_list.html', context)


def delete_task(request, task_id):
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

    if request.method == 'POST':
        client_id = request.POST.get('client_id')  # For edit
        data = request.POST

        # Collect all fields
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

        # Check uniqueness
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

        # === Handle errors ===
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
    return render(request, 'dm_head/register_client.html', {'clients': clients})


def delete_client(request, client_id):
    client = ClientRegister.objects.get(id=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully.')
    return redirect('register_client')


def register_work(request):
    works = WorkRegister.objects.all()

    work_data = []
    for work in works:
        has_lead_collection = work.clienttask_register_set.filter(task_name__icontains='Lead Collection').exists()
        work_data.append({
            'work': work,
            'has_lead_collection': has_lead_collection,
        })

    context = {'work_data': work_data}
    return render(request, 'dm_head/register_work.html', context)






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

        # Map input names to model fields
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


from django.http import JsonResponse, Http404

def get_client(request, client_id):
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
            'company_id': client.company.id if client.company else '9',
        }
        return JsonResponse(data)
    except ClientRegister.DoesNotExist:
        raise Http404("Client not found")



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



from itertools import chain

def get_available_tasks(request):
    logged_in_user = LogRegister_Details.objects.get(log_username=request.session.get('hid'))
    dm_head_profile = EmployeeRegister_Details.objects.filter(login=logged_in_user).first()
    company = dm_head_profile.company

    lead_tasks = Work_Task.objects.filter(company__isnull=True)
    company_tasks = Work_Task.objects.filter(company=company)

    combined_tasks = chain(lead_tasks, company_tasks)
    task_list = [{'id': t.id, 'name': t.task_name, 'description': t.task_description} for t in combined_tasks]

    return JsonResponse({'tasks': task_list})

