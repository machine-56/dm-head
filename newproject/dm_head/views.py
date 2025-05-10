import re
from django.shortcuts import redirect, render
from django.contrib import messages

from myapp.models import LogRegister_Details, BusinessRegister_Details, EmployeeRegister_Details
from .models import Work_Task, ClientRegister, WorkRegister, ClientTask_Register, LeadCategory_Register, LeadField_Register

from django.db import models
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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

        # check if it's common task
        is_common = Work_Task.objects.filter(task_name=task.task_name, company__isnull=True).exists()

        # allow editing task_name only if it's client specific
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

            # Check if same client-specific task already exists
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
        }
        return render(request, 'dm_head/field_page.html', context)
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









# the gets
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

