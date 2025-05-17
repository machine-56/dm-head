document.addEventListener('DOMContentLoaded', function () {
  // === View Task Details Modal ===
  document.querySelectorAll('.view-task-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const clientName = this.dataset.clientname;
      const description = this.dataset.description;
      const allocatedDate = this.dataset.date;
      const taskList = JSON.parse(this.dataset.tasks || '[]');

      document.getElementById('view_client_name').value = clientName;
     document.getElementById('view_allocated_date').value = allocatedDate;
      document.getElementById('view_description').value = description;

      const taskUl = document.getElementById('view_task_details');
      taskUl.innerHTML = '';
      taskList.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = task.name;
        if (task.categories?.length) {
          const ul = document.createElement('ul');
          task.categories.forEach(cat => {
            const subLi = document.createElement('li');
            subLi.textContent = cat;
            ul.appendChild(subLi);
          });
          li.appendChild(ul);
        }
        taskUl.appendChild(li);
      });

      new bootstrap.Modal(document.getElementById('viewTaskDetailsModal')).show();
    });
  });

  // === Assign to Executives Modal ===
  document.querySelectorAll('.assign-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const taskId = this.dataset.taskid;
      const taskName = this.dataset.taskname;
      const teamAllocId = this.dataset.teamallocid;
      const tlId = this.dataset.teamleadid;

      document.getElementById('assign_task_id').value = taskId;
      document.getElementById('assign_task_name_display').value = taskName;
      document.getElementById('team_allocation_id').value = teamAllocId;

      // Reset and conditionally show category dropdown
      const dropdownContainer = document.getElementById('lead_category_dropdown_container');
      const dropdown = document.getElementById('lead_category_dropdown');
      dropdown.innerHTML = '<option selected disabled>Select Category</option>';
      dropdownContainer.classList.add('d-none');

      if (taskName.toLowerCase().trim() === 'lead collection') {
        dropdownContainer.classList.remove('d-none');
        fetch(`/get-lead-categories-for-tl-task/${teamAllocId}/`)
          .then(res => res.json())
          .then(data => {
            data.categories.forEach(cat => {
              const opt = document.createElement('option');
              opt.value = cat.id;
              opt.textContent = cat.name;
              dropdown.appendChild(opt);
            });
          });
      }

      // Load executives
      fetch(`/get-employees-for-tl/${tlId}/`)
        .then(res => res.json())
        .then(data => {
          const execChecklist = document.getElementById('exec_checklist');
          execChecklist.innerHTML = '';
          if (!data.length) {
            execChecklist.innerHTML = '<em>No employees linked.</em>';
            return;
          }
          data.forEach(emp => {
            const div = document.createElement('div');
            div.className = 'form-check';
            div.innerHTML = `
              <input type="checkbox" name="executives" value="${emp.id}" class="form-check-input" id="exec-${emp.id}">
              <label class="form-check-label" for="exec-${emp.id}">${emp.name}</label>
            `;
            execChecklist.appendChild(div);
          });
        });

      new bootstrap.Modal(document.getElementById('assignExecModal')).show();
    });
  });

  // === Clear (preserve readonly) ===
  document.getElementById('clearAssignExecBtn').addEventListener('click', () => {
    const form = document.getElementById('assignExecForm');
    const taskName = document.getElementById('assign_task_name_display').value;
    form.reset();
    document.getElementById('assign_task_name_display').value = taskName;
    document.getElementById('lead_category_dropdown_container').classList.add('d-none');
  });

  // === Submit assign form ===
  document.getElementById('assignExecForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch('/assign-to-executives/', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          window.location.reload();
        } else {
          alert(data.message);
        }
      })
      .catch(err => {
        alert('An error occurred. Please try again.');
      });
  });
});
