document.addEventListener("DOMContentLoaded", function () {
    console.log('js loaded head verify page.js')
  document.querySelectorAll(".show-lead-details").forEach(btn => {
    btn.addEventListener("click", function () {
      const leadId = this.dataset.id;

      fetch(`/get-lead-details/${leadId}/`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            const ld = data.lead;
            document.getElementById("ld_name").textContent = ld.name;
            document.getElementById("ld_contact").textContent = ld.contact;
            document.getElementById("ld_email").textContent = ld.email;

            // Status badges
            document.getElementById("ld_verified").classList.toggle("text-success", ld.verified);
            document.getElementById("ld_verified").textContent = ld.verified ? "Verified" : "Unverified";

            document.getElementById("ld_waste").classList.toggle("text-danger", ld.waste);
            document.getElementById("ld_waste").textContent = ld.waste ? "Marked as waste" : "Not a waste";

            document.getElementById("ld_incomplete").classList.toggle("text-warning", ld.incomplete);
            document.getElementById("ld_incomplete").textContent = ld.incomplete ? "Incomplete" : "Not Marked as incomplete";

            // More fields
            const more = document.getElementById("ld_more");
            more.innerHTML = "";
            data.details.forEach(field => {
              const div = document.createElement("div");
              div.className = "mb-2 d-flex justify-content-between align-items-center";
              div.innerHTML = `<span>${field.field_name}</span><span>${field.field_data}</span>`;
              more.appendChild(div);
            });

            // Show offcanvas
            new bootstrap.Offcanvas(document.getElementById("leadDetailCanvas")).show();
          }
        })
        .catch(err => console.error("Failed to fetch lead:", err));
    });
  });

  //modal related js

  // Toggle logic
  const toggleSingleBtn = document.getElementById("toggleSingle");
  const toggleExcelBtn = document.getElementById("toggleExcel");
  const formSingle = document.getElementById("addLeadForm");
  const formExcel = document.getElementById("excelUploadForm");
  
  toggleSingleBtn.addEventListener("click", () => {
    formSingle.style.display = "block";
    formExcel.style.display = "none";
  });
  
  toggleExcelBtn.addEventListener("click", () => {
    formSingle.style.display = "none";
    formExcel.style.display = "block";
  });
  
  // Validation
  const emailInput = document.getElementById("lead_email");
  const contactInput = document.getElementById("lead_contact");
  const emailError = document.getElementById("email_error");
  const contactError = document.getElementById("contact_error");
  
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  const phoneRegex = /^\d{10}$/;
  
  function validateEmail() {
    const value = emailInput.value.trim();
    if (!value) {
      emailError.textContent = "Email is required.";
      return false;
    }
    if (!emailRegex.test(value)) {
      emailError.textContent = "Enter a valid email (e.g., user@example.com).";
      return false;
    }
    emailError.textContent = "";
    return true;
  }
  
  function validateContact() {
    const value = contactInput.value.trim();
    if (!value) {
      contactError.textContent = "Contact number is required.";
      return false;
    }
    if (!phoneRegex.test(value)) {
      contactError.textContent = "Enter a valid 10-digit phone number.";
      return false;
    }
    contactError.textContent = "";
    return true;
  }
  
  emailInput.addEventListener("input", validateEmail);
  contactInput.addEventListener("input", validateContact);
  
  //TODO: Submission logic (backend not linked yet)
  const form = document.getElementById("addLeadForm");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
  
    const isEmailValid = validateEmail();
    const isPhoneValid = validateContact();
    if (!isEmailValid || !isPhoneValid) return;
  
    alert("Form is valid. Backend submission will be implemented soon.");
    form.reset();
    bootstrap.Modal.getInstance(document.getElementById("addLeadModal"))?.hide();
  });

  //* change the status
  document.getElementById("statusApplyBtn").addEventListener("click", change_lead_status);

  function change_lead_status() {
    console.log("🔘 Status change button clicked");
  
    const selectedStatus = document.getElementById("statusAction").value;
    const checkboxes = document.querySelectorAll("input[name='selected_leads']:checked");
    const leadIds = Array.from(checkboxes).map(cb => cb.value);
  
    console.log("✅ Leads selected:", leadIds);
    console.log("✅ Selected Status:", selectedStatus);
  
    if (!selectedStatus || leadIds.length === 0) {
      console.warn("⚠️ Status or leads not selected");
      return;
    }
  
    fetch("/change-lead-status/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
      },
      body: JSON.stringify({ leads: leadIds, status: selectedStatus })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          console.log("✅ Backend updated successfully");
          window.location.reload();
        } else {
          console.error("❌ Backend responded with failure", data);
        }
      })
      .catch(err => console.error("❌ Request failed", err));
  }

  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  //* Table filtering
  const leadTable = $("#leadTable").DataTable({
    searching: false,
    ordering: true,
    paging: false,
    info: false,
    order: [],
    columnDefs: [{ orderable: false, targets: "nosort" }],
  });

  document.getElementById("searchInput").addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll("#leadTable tbody tr");
    rows.forEach((row) => {
      const rowText = row.innerText.toLowerCase();
      row.style.display = rowText.includes(filter) ? "" : "none";
    });
  });

  document.getElementById("clearSearch").addEventListener("click", function () {
    const input = document.getElementById("searchInput");
    input.value = "";
    const rows = document.querySelectorAll("#leadTable tbody tr");
    rows.forEach((row) => (row.style.display = ""));
  });

  //* filters
  function applyFiltersAndSearch() {
    const statusVal = document.getElementById("statusFilter").value;
    const empVal = document.getElementById("employeeFilter").value;
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;
    const searchQuery = document.getElementById("searchInput").value.toLowerCase();
    const rowLimit = parseInt(document.getElementById("rowLimit").value) || Infinity;
  
    const rows = document.querySelectorAll("#leadTable tbody tr");
    let shownCount = 0;
  
    rows.forEach(row => {
      let show = true;
      const statusText = row.querySelector("td:nth-child(6)")?.innerText.toLowerCase();
      const empId = row.querySelector("td:nth-child(2)")?.dataset.empId;
      const addedOn = row.querySelector("td:nth-child(2) small")?.innerText;
      const fromDate = row.querySelector("td:nth-child(2)")?.dataset.from;
      const toDate = row.querySelector("td:nth-child(2)")?.dataset.to;
      const rowText = row.innerText.toLowerCase();
  
      if (searchQuery && !rowText.includes(searchQuery)) show = false;
      if (empVal && empId !== empVal) show = false;
      if (statusVal) {
        const map = {
            "unverified": "unverified",
            "verified": "verified",
            "waste": "waste",
            "not_waste": "not a waste",
            "incomplete": "incomplete",
            "not_incomplete": "not marked as incomplete",
            "repeated": "repeated"
          };
        if (statusVal && statusText.trim() !== map[statusVal]) show = false;
  
      }
      const addedDate = new Date(addedOn);
      if (start && addedDate < new Date(start)) show = false;
      if (end && addedDate > new Date(end)) show = false;
  
      if (fromDate && start && new Date(fromDate) < new Date(start)) show = false;
      if (toDate && end && new Date(toDate) > new Date(end)) show = false;
  
      if (show && shownCount < rowLimit) {
        row.style.display = "";
        shownCount++;
      } else {
        row.style.display = "none";
      }
    });
  }
  
  updateFilterHeading();

  ["statusFilter", "employeeFilter", "startDate", "endDate", "searchInput", "rowLimit"].forEach(id => {
    document.getElementById(id).addEventListener("change", applyFiltersAndSearch);
    document.getElementById(id).addEventListener("input", applyFiltersAndSearch);
  });

    function updateFilterHeading() {
    const statusVal = document.getElementById("statusFilter").value;
    const heading = document.getElementById("filterHeading");
  
    let label = "All Leads";
    const labelMap = {
      "unverified": "Unverified Leads",
      "verified": "Verified Leads",
      "waste": "Wasted Leads",
      "not_waste": "Not Wasted Leads",
      "incomplete": "Incomplete Leads",
      "not_incomplete": "Not Incomplete Leads",
      "repeated": "Repeated Leads"
    };
  
    if (statusVal && labelMap[statusVal]) {
      label = labelMap[statusVal];
    }
  
    heading.textContent = label;
  }
  
  //!* Clear table Filters
  document.getElementById("resetFilters").addEventListener("click", function () {
    ["statusFilter", "employeeFilter", "startDate", "endDate", "searchInput", "rowLimit"].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = "";
    });
  
    applyFiltersAndSearch();
  });

  applyFiltersAndSearch();

});


document.getElementById("checkAll").addEventListener("change", function () {
  const isChecked = this.checked;
  document.querySelectorAll("#leadTable tbody tr").forEach(row => {
    if (row.style.display !== "none") {
      const checkbox = row.querySelector("input[type='checkbox']");
      if (checkbox) checkbox.checked = isChecked;
    }
  });
});


//* rowlimiter
document.getElementById("rowLimit").addEventListener("change", function () {
  const selected = parseInt(this.value);
  const rows = document.querySelectorAll("#leadTable tbody tr");
  let shown = 0;
  rows.forEach(row => {
    if (shown < selected) {
      row.style.display = "";
      shown++;
    } else {
      row.style.display = "none";
    }
  });
});


//!* print
document.getElementById("pdfBtn").addEventListener("click", function () {
  document.querySelectorAll('.print-hide').forEach(el => el.style.display = 'none');
  
  const tableClone = document.getElementById("leadTable").cloneNode(true);
  tableClone.querySelectorAll("tbody tr").forEach(row => {
    if (row.style.display === "none") row.remove();
  });

  const wrapper = document.createElement("div");
  wrapper.appendChild(tableClone);

  html2pdf().set({
    margin: 0.5,
    filename: `Leads_${new Date().toISOString().split("T")[0]}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  }).from(wrapper).save().then(() => {
    document.querySelectorAll('.print-hide').forEach(el => el.style.display = '');
  });
});