function populateWorkForm(clientId) {
    fetch(`/dm_head/get-client/${clientId}/`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('#createWorkForm [name="client_id"]').value = clientId;
            document.querySelector('#createWorkForm [name="client_name"]').value = data.client_name;
            document.querySelector('#createWorkForm [name="client_business_name"]').value = data.client_business_name;

            // Inject task checkboxes (2 per row)
            const taskContainer = document.getElementById('taskCheckboxes');
            taskContainer.innerHTML = '';
            const tasks = data.tasks || ['Lead Collection', 'Other Task']; // fallback if needed
            tasks.forEach((task, index) => {
                if (index % 2 === 0) {
                    taskContainer.innerHTML += `<div class="w-100"></div>`;
                }
                taskContainer.innerHTML += `
                    <div class="col-md-6 mb-2">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="task_choices" value="${task}">
                            <label class="form-check-label">${task}</label>
                        </div>
                    </div>
                `;
            });

            const modal = new bootstrap.Modal(document.getElementById('createWorkModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error loading client or tasks:', error);
            alert('Failed to load client info.');
        });
}

// Add/remove additional task input
document.getElementById('addTaskBtn').addEventListener('click', function () {
    const container = document.getElementById('additionalTaskContainer');
    if (container.style.display === 'none') {
        container.style.display = 'block';
        addTaskBtn.classList.remove('btn-outline-success');
        addTaskBtn.classList.add('btn-outline-danger');
        addTaskBtn.innerHTML = '-';
    } else {
        container.style.display = 'none';
        addTaskBtn.classList.remove('btn-outline-danger');
        addTaskBtn.classList.add('btn-outline-success');
        addTaskBtn.innerHTML = '+';
        container.querySelector('input').value = '';
    }
});
// Load available tasks from DB (excluding company tasks)
function loadTasks(companyId) {
    fetch('/dm_head/get-tasks/')
        .then(res => res.json())
        .then(data => {
            const taskContainer = document.getElementById('taskList');
            taskContainer.innerHTML = '';
            data.tasks.forEach(task => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = task.id;
                checkbox.name = 'task_ids[]';
                checkbox.classList.add('form-check-input');
                const label = document.createElement('label');
                label.classList.add('form-check-label', 'ms-2');
                label.textContent = `${task.name} (${task.description || 'No description'})`;
                const wrapper = document.createElement('div');
                wrapper.classList.add('form-check', 'mb-1');
                wrapper.appendChild(checkbox);
                wrapper.appendChild(label);
                taskContainer.appendChild(wrapper);
            });
        });
}

// Add a new company-specific task
function addCompanyTask(companyId) {
    const taskName = document.getElementById('newTaskName').value.trim();
    const taskDescription = document.getElementById('newTaskDesc').value.trim();

    if (!taskName) {
        alert('Task name is required.');
        return;
    }

    const formData = new FormData();
    formData.append('task_name', taskName);
    formData.append('task_description', taskDescription);
    formData.append('company_id', companyId);

    fetch('/dm_head/add-company-task/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById('newTaskName').value = '';
            document.getElementById('newTaskDesc').value = '';
            loadTasks(companyId);
        }
    })
    .catch(() => alert('Error adding new task.'));
}

// Submit the work creation form
function submitWork(companyId) {
    const form = document.getElementById('createWorkForm');
    const formData = new FormData(form);
    formData.append('company_id', companyId);

    fetch('/dm_head/create-work/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(() => alert('Error submitting work.'));
}

// Initialize modal when opened
function setupWorkModal(companyId) {
    loadTasks(companyId);

    document.getElementById('addTaskButton').addEventListener('click', () => {
        addCompanyTask(companyId);
    });

    document.getElementById('createWorkButton').addEventListener('click', () => {
        submitWork(companyId);
    });
}

// OPTIONAL: Reset form and listeners when modal closes
document.getElementById('registerWorkModal').addEventListener('hidden.bs.modal', () => {
    document.getElementById('createWorkForm').reset();
    document.getElementById('taskList').innerHTML = '';
});
const addTaskBtn = document.getElementById('addTaskBtn');
const additionalTaskContainer = document.getElementById('additionalTaskContainer');

addTaskBtn.addEventListener('click', () => {
    if (additionalTaskContainer.style.display === 'none') {
        additionalTaskContainer.style.display = 'block';
        
    } else {
        additionalTaskContainer.style.display = 'none';
        
    }
});
