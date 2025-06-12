let dataTable;

document.addEventListener("DOMContentLoaded", function () {
  const rowLimitElement = document.getElementById("rowLimit");
  const rowLimitValue = rowLimitElement ? parseInt(rowLimitElement.value) || 10 : 10;

  dataTable = $('#leadTable').DataTable({
    paging: true,
    searching: false,
    ordering: true,
    order: [],
    lengthChange: false,
    pageLength: rowLimitValue,
    columnDefs: [{ orderable: false, targets: 0 }]
  });

  rowLimitElement?.addEventListener("change", function () {
    const val = parseInt(this.value) || 10;
    dataTable.page.len(val).draw();
  });

  setupEventListeners();
  applyFilters();
  filterCategoryByClient();
});


function setupEventListeners() {
  const filterFields = ["clientFilter", "categoryFilter", "employeeFilter", "fromDate", "toDate", "searchInput"];

  // Filters
  filterFields.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", applyFilters);
      el.addEventListener("change", applyFilters);
    }
  });

  // Clear filters
  document.getElementById("clearFilters")?.addEventListener("click", () => {
    filterFields.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = "";
    });
    applyFilters();
  });

  // Clear search
  document.getElementById("clearSearch")?.addEventListener("click", () => {
    document.getElementById("searchInput").value = "";
    applyFilters();
  });

  // Select all visible rows
  document.getElementById("checkAll")?.addEventListener("change", function () {
    const checked = this.checked;
    document.querySelectorAll("#leadTable tbody tr").forEach(row => {
      if ($(row).is(":visible")) {
        const cb = row.querySelector("input[type='checkbox']");
        if (cb) cb.checked = checked;
      }
    });
  });

  // Transfer leads
 document.getElementById("transferBtn")?.addEventListener("click", function () {
  console.log("🔁 Transfer button clicked");

  // Check for checkbox selection
  const selectedCheckboxes = document.querySelectorAll("input[name='selected_leads']:checked");
  const selected = Array.from(selectedCheckboxes).map(cb => cb.value);

  if (selected.length === 0) {
    alert("Select at least one lead.");
    return;
  }

  const csrfEl = document.querySelector("[name=csrfmiddlewaretoken]");
  if (!csrfEl) {
    return;
  }

  const csrfToken = csrfEl.value;
  fetch("/transfer-selected-leads/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ leads: selected })
  })
    .then(res => {
      return res.json();
    })
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert("Transfer failed: " + (data.message || "Unknown error"));
      }
    })
    .catch(err => {
      alert("Something went wrong during transfer.");
    });
});


  // PDF export
  document.getElementById("pdfBtn")?.addEventListener("click", exportPDF);

  // EXCEL export
document.getElementById("excelBtn").addEventListener("click", function () {
  const clientDropdown = document.getElementById("clientFilter");
  const selectedClient = clientDropdown?.options[clientDropdown.selectedIndex]?.text;
  const clientName = clientDropdown?.value ? selectedClient.trim().replace(/\s+/g, "_") : null;
  const filename = clientName ? `${clientName}_leads.xlsx` : `leads.xlsx`;

  const table = document.getElementById("leadTable");
  const visibleRows = Array.from(table.querySelectorAll("tbody tr")).filter(row => row.style.display !== "none");

  // Build new array with clean headers and split values
  const data = [
    ["Collected By", "Date", "Name", "Source", "Email", "Phone", "Status"]
  ];

  visibleRows.forEach(row => {
    const cells = row.querySelectorAll("td");

    // Extract and split values
    const collectedByText = cells[1]?.innerText.split("\n");
    const nameSourceText = cells[2]?.innerText.split("\n");
    const contactText = cells[3]?.innerText.split("\n");
    const statusText = cells[4]?.innerText;

    data.push([
      collectedByText?.[0] || "",
      collectedByText?.[1] || "",
      nameSourceText?.[0] || "",
      nameSourceText?.[1] || "",
      contactText?.[0] || "",
      contactText?.[1] || "",
      statusText || ""
    ]);
  });

  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(data);
  XLSX.utils.book_append_sheet(wb, ws, "Leads");

  XLSX.writeFile(wb, filename);
})

  document.getElementById("clientFilter")?.addEventListener("change", filterCategoryByClient);
}

document.getElementById("clientFilter")?.addEventListener("change", () => {
  document.getElementById("categoryFilter").value = "";
  filterCategoryByClient();
  applyFilters();
});


function applyFilters() {
  const client = document.getElementById("clientFilter").value;
  const category = document.getElementById("categoryFilter").value;
  const emp = document.getElementById("employeeFilter").value;
  const from = new Date(document.getElementById("fromDate").value);
  const to = new Date(document.getElementById("toDate").value);
  const search = document.getElementById("searchInput").value.toLowerCase();

  let visibleCount = 0;

  dataTable.rows().every(function () {
    const row = this.node();
    const rowClient = row.dataset.client;
    const rowCategory = row.dataset.category;
    const rowEmp = row.dataset.employee;
    const rowDate = new Date(row.dataset.date);
    const text = row.innerText.toLowerCase();

    let show = true;
    if (client && rowClient !== client) show = false;
    if (category && rowCategory !== category) show = false;
    if (emp && rowEmp !== emp) show = false;
    if (from && rowDate < from) show = false;
    if (to && rowDate > to) show = false;
    if (search && !text.includes(search)) show = false;

    $(row).toggle(show);
    if (show) visibleCount++;

    const noMsg = document.getElementById("noResultsMessage");
    const tableWrapper = document.getElementById("tableWrapper");
    const infoElement = document.querySelector(".dataTables_info");
    const paginateElement = document.querySelector(".dataTables_paginate");
      
    if (visibleCount === 0) {
      if (noMsg) noMsg.style.display = "block";
      if (tableWrapper) tableWrapper.style.display = "none";
      if (infoElement) infoElement.style.display = "none";
      if (paginateElement) paginateElement.style.display = "none";
    } else {
      if (noMsg) noMsg.style.display = "none";
      if (tableWrapper) tableWrapper.style.display = "";
      if (infoElement) infoElement.style.display = "";
      if (paginateElement) paginateElement.style.display = "";
    }

  });

  const noMsg = document.getElementById("noResultsMessage");
  if (noMsg) {
    noMsg.style.display = visibleCount === 0 ? "block" : "none";
  }

  dataTable.draw();
}


function exportPDF() {
  const table = document.getElementById("leadTable").cloneNode(true);
  table.querySelectorAll("thead th:first-child, tbody td:first-child").forEach(el => el.remove());

  const visibleRows = table.querySelectorAll("tbody tr");
  visibleRows.forEach(row => {
    if (row.style.display === "none") row.remove();
  });

  const wrapper = document.createElement("div");

  const title = document.createElement("h3");
  title.textContent = "Verified Leads for Transfer";
  title.style.textAlign = "center";
  title.style.marginBottom = "15px";
  wrapper.appendChild(title);

  table.classList.add("table", "table-bordered", "table-sm");
  table.style.fontSize = "10px";
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";
  wrapper.appendChild(table);

  html2pdf().set({
    margin: [0.4, 0.2],
    filename: `Leads_${new Date().toISOString().split("T")[0]}.pdf`,
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "letter", orientation: "portrait" }
  }).from(wrapper).save();
}

function filterCategoryByClient() {
  const selectedClientId = document.getElementById("clientFilter")?.value;
  const categoryDropdown = document.getElementById("categoryFilter");
  if (!categoryDropdown) return;

  // Always show "All"
  const allOption = categoryDropdown.querySelector("option[value='']");
  allOption.style.display = "";

  // Reset selection to "All"
  categoryDropdown.value = "";

  // Hide all category options
  categoryDropdown.querySelectorAll("option").forEach(opt => {
    if (opt.value !== "") opt.style.display = "none";
  });

  if (!selectedClientId) return;

  // Show only options related to this client
  categoryDropdown.querySelectorAll(".client-" + selectedClientId).forEach(opt => {
    opt.style.display = "";
  });
}


