document.addEventListener("DOMContentLoaded", function () {
  const table = $('#dataBankTable').DataTable({
    paging: true,
    ordering: true,
    searching: false,
    lengthChange: false,
    pageLength: parseInt(document.getElementById('rowCount')?.value || 25)
  });

  // Row count change
  const rowCountEl = document.getElementById('rowCount');
  rowCountEl?.addEventListener('change', function () {
    table.page.len(parseInt(this.value)).draw();
  });

  // Search input
  document.getElementById('searchInput')?.addEventListener('keyup', function () {
    const val = this.value.toLowerCase();
    $('#dataBankTable tbody tr').each(function () {
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

  // Category dropdown on client selection
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

  // All dropdown filters
  ['categorySelect', 'statusSelect', 'startDate', 'endDate'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', applyFilters);
    }
  });

  document.getElementById('hrFilter')?.addEventListener('change', applyFilters);

  // Clear filters → Reload the page
  document.getElementById('clearFilters')?.addEventListener('click', function () {
    window.location.reload(); // works cleanest for full reset
  });

  function applyFilters() {
    const client = document.getElementById('clientSelect')?.value;
    const category = document.getElementById('categorySelect')?.value;
    const status = document.getElementById('statusSelect')?.value?.toLowerCase();
    const start = document.getElementById('startDate')?.value;
    const end = document.getElementById('endDate')?.value;
    const hr = document.getElementById('hrFilter')?.value;

    console.log('Filters:', { client, category, status, start, end, hr });

    $('#dataBankTable tbody tr').each(function () {
      const row = $(this);
      const rowClient = row.data('client-id')?.toString();
      const rowCategory = row.data('category-id')?.toString();
      const rowStatus = row.data('status')?.toLowerCase();
      const rowDate = row.data('added')?.toString();
      const rowHr = row.data('hr')?.toString();
      const isAllocated = row.data('allocated')?.toString() === '1';

      let visible = true;

      if (client && rowClient !== client) visible = false;
      if (category && rowCategory !== category) visible = false;
      if (status && rowStatus !== status) visible = false;

      if (start && (!rowDate || rowDate < start)) {
        visible = false;
        console.log(`Date before start: ${rowDate} < ${start}`);
      }

      if (end && (!rowDate || rowDate > end)) {
        visible = false;
        console.log(`Date after end: ${rowDate} > ${end}`);
      }

      if (hr === 'all') {
        // Show all (do nothing)
      } else if (hr === '') {
        if (!isAllocated) {
          visible = false;
          console.log('Hiding unallocated lead for HR = All');
        }
      } else if (hr === 'none') {
        if (isAllocated) {
          visible = false;
          console.log('Hiding allocated lead for HR = None');
        }
      } else {
        if (!isAllocated || rowHr !== hr) {
          visible = false;
          console.log(`HR mismatch or unallocated: rowHr=${rowHr}, expected=${hr}`);
        }
      }

      row.toggle(visible);
    });

    toggleNoData();
  }

  function toggleNoData() {
    const rowsVisible = $('#dataBankTable tbody tr:visible').length;
    $('#noDataMessage').toggle(rowsVisible === 0);
  }
});
