console.log('tl new works js')
document.addEventListener('DOMContentLoaded', () => {
  const modal = new bootstrap.Modal(document.getElementById('taskDetailModal'));

  document.querySelectorAll('.view-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById('modalClientName').value = btn.dataset.client || '';
      document.getElementById('modalAssignDate').value = btn.dataset.assign || '';
      document.getElementById('modalTaskName').value = btn.dataset.name || '';
      document.getElementById('modalTarget').value = btn.dataset.target || '';
      document.getElementById('modalStartDate').value = btn.dataset.start || '';
      document.getElementById('modalEndDate').value = btn.dataset.end || '';
      document.getElementById('modalDescription').value = btn.dataset.description || '';

      const fileLink = btn.dataset.file;
      const linkEl = document.getElementById('modalDownloadLink');
      if (fileLink) {
        linkEl.href = fileLink;
        linkEl.parentElement.style.display = 'block';
      } else {
        linkEl.parentElement.style.display = 'none';
      }

      modal.show();
    });
  });
});
