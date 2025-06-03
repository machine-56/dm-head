
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('addLeadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    fetch("{% url 'add_lead_manual' %}", {
      method: 'POST',
      body: data
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        alert("Failed to add lead.");
      }
    });
  });
  
  document.querySelectorAll('.show-lead-details').forEach(btn => {
    btn.addEventListener('click', () => {
      const leadId = btn.dataset.id;
      fetch(`/get-lead-details/${leadId}/`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            const l = data.lead;
            document.getElementById('ld_name').innerText = l.name;
            document.getElementById('ld_contact').innerText = l.contact;
            document.getElementById('ld_email').innerText = l.email;
            document.getElementById('ld_verified').innerText = l.verified ? 'Verified' : 'Unverified';
            document.getElementById('ld_verified').className = l.verified ? 'badge bg-success' : 'badge bg-danger';
            document.getElementById('ld_waste').style.display = l.waste ? 'inline-block' : 'none';
            document.getElementById('ld_incomplete').style.display = l.incomplete ? 'inline-block' : 'none';
  
            const detailsDiv = document.getElementById('ld_more');
            detailsDiv.innerHTML = '';
            data.details.forEach(item => {
              const p = document.createElement('p');
              p.innerHTML = `<strong>${item.field_name}</strong> : ${item.field_data}`;
              detailsDiv.appendChild(p);
            });
  
            new bootstrap.Offcanvas(document.getElementById('leadDetailCanvas')).show();
          }
        });
    });
  });
  
  
  // table head sorting
  $(document).ready(function () {
    const leadTable = $('#leadTable').DataTable({
      searching: false,
      ordering: true,
      paging: false,
      info: false,
      order: [],
      columnDefs: [
        { orderable: false, targets: 'nosort' }
      ]
    });
  
  document.getElementById("searchInput").addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll("#leadTable tbody tr");
  
    rows.forEach(row => {
      const rowText = row.innerText.toLowerCase();
      row.style.display = rowText.includes(filter) ? "" : "none";
    });
  });
  
  document.getElementById("clearSearch").addEventListener("click", function () {
    const input = document.getElementById("searchInput");
    input.value = "";
    const rows = document.querySelectorAll("#leadTable tbody tr");
    rows.forEach(row => (row.style.display = ""));
  });
  
  });
});




