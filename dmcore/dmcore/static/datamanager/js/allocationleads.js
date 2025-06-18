document.addEventListener("DOMContentLoaded", function () {
  const table = $('#allocationLeadsTable').DataTable({
    paging: true,
    ordering: true,
    searching: false,
    lengthChange: false,
    pageLength: parseInt(document.getElementById('rowCount')?.value || 25)
  });

  // Row count change
  document.getElementById('rowCount')?.addEventListener('change', function () {
    table.page.len(parseInt(this.value)).draw();
  });

  // Search input
  document.getElementById('searchInput')?.addEventListener('keyup', function () {
    const val = this.value.toLowerCase();
    $('#allocationLeadsTable tbody tr').each(function () {
      $(this).toggle($(this).text().toLowerCase().includes(val));
    });
    toggleNoData();
  });

  // Clear search input
  document.getElementById('clearSearch')?.addEventListener('click', function () {
    const input = document.getElementById('searchInput');
    if (input) {
      input.value = '';
      input.dispatchEvent(new Event('keyup'));
    }
  });

  // Client → Category dynamic loading
  document.getElementById('clientSelect')?.addEventListener('change', function () {
    const clientId = this.value;
    const categorySelect = document.getElementById('categorySelect');
    categorySelect.innerHTML = '<option value="">All</option>';

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

  // All filter listeners
  ['clientSelect', 'categorySelect', 'executiveSelect', 'statusSelect', 'startDate', 'endDate', 'hrFilter'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', applyFilters);
  });

  // Apply filters on load
  applyFilters();

  // Clear Filters button
  document.getElementById('clearFilters')?.addEventListener('click', function () {
    document.getElementById('clientSelect').selectedIndex = 0;
    document.getElementById('categorySelect').selectedIndex = 0;
    document.getElementById('executiveSelect').selectedIndex = 0;
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('statusSelect').value = 'Not Allocated';
    document.getElementById('hrFilter').value = 'none';
    applyFilters();
  });

  // Select All
  document.getElementById('selectAll')?.addEventListener('change', function () {
    const checked = this.checked;
    document.querySelectorAll('#allocationLeadsTable tbody input[type="checkbox"]')
      .forEach(cb => cb.checked = checked);
    updateSelectedCount();
  });

  // Per-row checkbox update
  document.querySelectorAll('#allocationLeadsTable tbody').forEach(tbody => {
    tbody.addEventListener('change', updateSelectedCount);
  });

  // Allocate button
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
      body: JSON.stringify({
        leads: selectedLeads,
        hr_id: selectedHr
      })
    })
      .then(res => res.json())
      .then(data => {
        showToast(data.message, data.success ? 'success' : 'danger');
        if (data.success) {
          setTimeout(() => window.location.reload(), 3500);
        }
      })
      .catch(() => alert('Something went wrong.'));
  });

  function updateSelectedCount() {
    const count = document.querySelectorAll('#allocationLeadsTable tbody input[type="checkbox"]:checked').length;
    document.getElementById('selectedCount').textContent = count;
  }

function applyFilters() {
  const client = document.getElementById('clientSelect')?.value;
  const category = document.getElementById('categorySelect')?.value;
  const executive = document.getElementById('executiveSelect')?.value;
  const status = document.getElementById('statusSelect')?.value?.toLowerCase();
  const hr = document.getElementById('hrFilter')?.value;
  const start = document.getElementById('startDate')?.value;
  const end = document.getElementById('endDate')?.value;

  $('#allocationLeadsTable tbody tr').each(function () {
    const row = $(this);
    const rowClient = row.data('client-id')?.toString();
    const rowCategory = row.data('category-id')?.toString();
    const rowStatus = row.data('status')?.toLowerCase();
    const rowExec = row.data('executive-id')?.toString();
    const rowHr = row.data('hr')?.toString();
    const rowDate = row.data('added')?.toString();
    const isAllocated = row.data('allocated')?.toString() === '1';

    let visible = true;

    if (client && rowClient !== client) visible = false;
    if (category && rowCategory !== category) visible = false;
    if (executive && rowExec !== executive) visible = false;
    if (start && (!rowDate || rowDate < start)) visible = false;
    if (end && (!rowDate || rowDate > end)) visible = false;

    if (hr === 'none') {
      if (isAllocated) visible = false;
      if (status && rowStatus !== status) visible = false;
    } else if (hr === '') {
      if (!isAllocated) visible = false;
    } else {
      if (!isAllocated || rowHr !== hr) visible = false;
    }

    row.toggle(visible);
  });

  toggleNoData();
}


  function toggleNoData() {
    const visibleRows = $('#allocationLeadsTable tbody tr:visible').length;
    $('#noDataMessage').toggle(visibleRows === 0);
  }
});

function openLeadDetails(leadId) {
  fetch(`/get_lead_details/${leadId}/`)
    .then(response => response.json())
    .then(data => {
      document.getElementById('leadName').textContent = data.lead.name || '-';
      document.getElementById('leadEmail').textContent = data.lead.email || '-';
      document.getElementById('leadContact').textContent = data.lead.contact || '-';
      document.getElementById('clientName').textContent = data.client.name || '-';
      document.getElementById('clientInfo').textContent = data.client.info || '-';

      const moreDetailsDiv = document.getElementById('leadExtraDetails');
      moreDetailsDiv.innerHTML = '';
      if (data.more_details?.length) {
        data.more_details.forEach(item => {
          const p = document.createElement('p');
          p.innerHTML = `<i class="bi bi-file-text"></i> ${item.label} : ${item.value}`;
          moreDetailsDiv.appendChild(p);
        });
      } else {
        moreDetailsDiv.innerHTML = '<p>No extra details found.</p>';
      }

      const followupDiv = document.getElementById('followupTrack');
      followupDiv.innerHTML = data.followups?.length
        ? `<div>Collected By: ${data.followups[0].collected_by}</div>`
        : '<div>No followup data.</div>';

      const historyDiv = document.getElementById('historyTrack');
      historyDiv.innerHTML = data.history?.length
        ? `<div>Added on: ${data.history[0].date} at ${data.history[0].time}</div>`
        : '<div>No history data.</div>';
    })
    .catch(() => {
      console.error('Failed to load lead details.');
    });
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
