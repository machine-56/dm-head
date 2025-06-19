document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM ready. Initializing filters...");

  const table = $('#allocationLeadsTable').DataTable({
    paging: true,
    ordering: true,
    searching: false,
    lengthChange: false,
    pageLength: parseInt(document.getElementById('rowCount')?.value || 25)
  });

  document.getElementById('rowCount')?.addEventListener('change', function () {
    table.page.len(parseInt(this.value)).draw();
  });

  document.getElementById('searchInput')?.addEventListener('keyup', function () {
    const val = this.value.toLowerCase();
    $('#allocationLeadsTable tbody tr').each(function () {
      $(this).toggle($(this).text().toLowerCase().includes(val));
    });
    toggleNoData();
  });

  document.getElementById('clearSearch')?.addEventListener('click', function () {
    const input = document.getElementById('searchInput');
    input.value = '';
    applyFilters();
  });



  document.getElementById('clientSelect')?.addEventListener('change', function () {
    const clientId = this.value;
    const categorySelect = document.getElementById('categorySelect');
    categorySelect.innerHTML = '<option value="">All</option>';
    console.log(`Client selected: ${clientId}`);

    if (clientId) {
      fetch(`/get-categories-for-client/${clientId}/`)
        .then(res => res.json())
        .then(data => {
          data.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = c.name;
            categorySelect.appendChild(opt);
          });
          applyFilters();
        });
    } else {
      applyFilters();
    }
  });

  ['clientSelect', 'categorySelect', 'executiveSelect', 'statusSelect', 'startDate', 'endDate', 'hrFilter'].forEach(id => {
    document.getElementById(id)?.addEventListener('change', applyFilters);
  });

  document.getElementById('clearFilters')?.addEventListener('click', function () {
    console.log("Clearing all filters...");
    document.getElementById('clientSelect').selectedIndex = 0;
    document.getElementById('categorySelect').selectedIndex = 0;
    document.getElementById('executiveSelect').selectedIndex = 0;
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('statusSelect').value = 'Not Allocated';
    document.getElementById('hrFilter').selectedIndex = 0;
    applyFilters();
  });

  document.getElementById('selectAll')?.addEventListener('change', function () {
    const checked = this.checked;
    document.querySelectorAll('#allocationLeadsTable tbody input[type="checkbox"]').forEach(cb => {
      if (!cb.disabled) cb.checked = checked;
    });
    updateSelectedCount();
  });

  document.querySelectorAll('#allocationLeadsTable tbody').forEach(tbody => {
    tbody.addEventListener('change', updateSelectedCount);
  });

  document.getElementById('allocateBtn')?.addEventListener('click', function () {
    const selectedLeads = Array.from(document.querySelectorAll('#allocationLeadsTable tbody input[type="checkbox"]:checked'))
      .map(cb => cb.dataset.leadId);
    const selectedHr = document.getElementById('selectHrAllocate')?.value;

    if (!selectedHr || selectedLeads.length === 0) {
      alert('Please select at least one lead and an HR.');
      return;
    }

    fetch('/allocate-leads/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ leads: selectedLeads, hr_id: selectedHr })
    })
      .then(res => res.json())
      .then(data => {
        showToast(data.message, data.success ? 'success' : 'danger');
        if (data.success) setTimeout(() => window.location.reload(), 1600);
      })
      .catch(() => alert('Something went wrong.'));
  });

  applyFilters();

function applyFilters() {
  const client = document.getElementById('clientSelect')?.value;
  const category = document.getElementById('categorySelect')?.value;
  const executive = document.getElementById('executiveSelect')?.value;
  const status = document.getElementById('statusSelect')?.value?.toLowerCase();
  const hr = document.getElementById('hrFilter')?.value;
  const start = document.getElementById('startDate')?.value;
  const end = document.getElementById('endDate')?.value;

  console.log("Applying filters →", { client, category, executive, status, hr, start, end });

  $('#allocationLeadsTable tbody tr').each(function () {
    const row = $(this);
    const rowClient = String(row.data('client-id'));
    const rowCategory = String(row.data('category-id'));
    const rowExec = String(row.data('executive-id'));
    const rowStatus = String(row.data('status')).toLowerCase();
    const rowHr = String(row.data('hr'));
    const rowDate = row.data('added');
    const isAllocated = String(row.data('allocated')) === '1';

    let visible = true;

    //? Stack filters
    if (client && rowClient !== client) visible = false;
    if (category && rowCategory !== category) visible = false;
    if (executive && rowExec !== executive) visible = false;
    if (start && (!rowDate || rowDate < start)) visible = false;
    if (end && (!rowDate || rowDate > end)) visible = false;
    if (!status && !hr) {
      if (rowStatus !== 'not allocated') visible = false;
    } else {
      if (status && rowStatus !== status) visible = false;
      if (hr && hr !== 'none' && rowHr !== hr) visible = false;
    }

    row.toggle(visible);
  });

  toggleNoData();
}


  function toggleNoData() {
    const visibleRows = $('#allocationLeadsTable tbody tr:visible').length;
    document.getElementById('noDataMessage').style.display = visibleRows === 0 ? 'block' : 'none';
  }

  function updateSelectedCount() {
    const count = document.querySelectorAll('#allocationLeadsTable tbody input[type="checkbox"]:checked').length;
    document.getElementById('selectedCount').textContent = count;
  }

  function showToast(message, type = 'success') {
    const toastEl = document.getElementById('allocationToast');
    const toastMsg = document.getElementById('allocationToastMessage');
    toastMsg.textContent = message;
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    new bootstrap.Toast(toastEl).show();
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
