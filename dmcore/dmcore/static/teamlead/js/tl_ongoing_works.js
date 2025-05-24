console.log('js loaded');  // !========delete this line =============

document.addEventListener('DOMContentLoaded', () => {
  // Set progress bar widths
  document.querySelectorAll('.progress-bar').forEach(bar => {
    const value = parseInt(bar.dataset.progress || '0');
    bar.style.width = `${value}%`;
    bar.innerText = `${value}%`;
    bar.setAttribute('aria-valuenow', value);
  });

  // View modal logic
  document.querySelectorAll('.view-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      console.log("[VIEW MODAL DATA] ==========");  // !========delete this line =============
      console.log("Client:", btn.dataset.client);   // !========delete this line =============
      console.log("Allocated:", btn.dataset.assign); // !========delete this line =============
      console.log("Accepted:", btn.dataset.accept);  // !========delete this line =============
      console.log("Task Name:", btn.dataset.name);   // !========delete this line =============
      console.log("Target:", btn.dataset.target);    // !========delete this line =============
      console.log("Achieved:", btn.dataset.achieved); // !========delete this line =============
      console.log("Start Date:", btn.dataset.start); // !========delete this line =============
      console.log("End Date:", btn.dataset.end);     // !========delete this line =============
      console.log("Description:", btn.dataset.description); // !========delete this line =============
      console.log("File:", btn.dataset.file);        // !========delete this line =============

      document.getElementById('v_client').value = btn.dataset.client || '';
      document.getElementById('v_allocated').value = btn.dataset.assign || '';
      document.getElementById('v_accepted').value = btn.dataset.accept || '';
      document.getElementById('v_taskname').value = btn.dataset.name || '';
      document.getElementById('v_target').value = btn.dataset.target || '';
      document.getElementById('v_achieved').value = btn.dataset.achieved || '';
      document.getElementById('v_start').value = btn.dataset.start || '';
      document.getElementById('v_end').value = btn.dataset.end || '';
      document.getElementById('v_description').value = btn.dataset.description || '';

      const file = btn.dataset.file;
      const box = document.getElementById('v_file_box');
      const link = document.getElementById('v_file_link');
      if (file) {
        link.href = file;
        box.style.display = 'block';
      } else {
        box.style.display = 'none';
      }

      new bootstrap.Modal(document.getElementById('viewTaskModal')).show();
    });
  });

  // Add Daily Work Modal (only for normal tasks)
  document.querySelectorAll('.add-daily-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const taskName = btn.dataset.name || '';
      const assignId = btn.dataset.assignid || '';

      document.getElementById('d_taskname').value = taskName;

      // Optional: store assign ID in hidden input
      const hidden = document.getElementById('task_assign_id');
      if (hidden) hidden.value = assignId;

      new bootstrap.Modal(document.getElementById('addDailyModal')).show();
    });
  });
});
