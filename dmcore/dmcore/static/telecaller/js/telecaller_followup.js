document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const statusFilter = document.getElementById("statusFilter");
  const fromDate = document.getElementById("fromDate");
  const toDate = document.getElementById("toDate");
  const nextFollowUpDate = document.getElementById("nextFollowUpDate");
  const rowCount = document.getElementById("rowCount");
  const tableBody = document.getElementById("leadTableBody");
  const paginationContainer = document.querySelector(".pagination");
  const offcanvas = new bootstrap.Offcanvas('#updateOffcanvas');
  let rows = Array.from(tableBody.querySelectorAll("tr"));

  function filterTable() {
    const statusVal = statusFilter.value.toLowerCase();
    const from = new Date(fromDate.value);
    const to = new Date(toDate.value);
    const nextDate = new Date(nextFollowUpDate.value);
    const query = searchInput.value.toLowerCase();
    let visibleRows = 0;

    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const rowStatus = row.children[7].textContent.toLowerCase();
      const allocDate = new Date(row.children[8].textContent);
      const followDate = new Date(row.children[9].textContent);

      const matchSearch = text.includes(query);
      const matchStatus = !statusVal || rowStatus.includes(statusVal);
      const matchFrom = !fromDate.value || allocDate >= from;
      const matchTo = !toDate.value || allocDate <= to;
      const matchNext = !nextFollowUpDate.value || followDate.toDateString() === nextDate.toDateString();

      if (matchSearch && matchStatus && matchFrom && matchTo && matchNext) {
        row.style.display = "";
        visibleRows++;
      } else {
        row.style.display = "none";
      }
    });

    document.getElementById("noLeadsRow")?.remove();
    if (visibleRows === 0) {
      const noRow = document.createElement("tr");
      noRow.id = "noLeadsRow";
      noRow.innerHTML = `<td colspan="7" class="text-center text-white">No Leads Found</td>`;
      tableBody.appendChild(noRow);
    }

    paginate();
  }

  function paginate() {
    const perPage = parseInt(rowCount.value);
    const visible = rows.filter(r => r.style.display !== "none");
    const pages = Math.ceil(visible.length / perPage);

    paginationContainer.innerHTML = "";

    visible.forEach((r, i) => {
      r.style.display = (i < perPage) ? "" : "none";
    });

    for (let i = 1; i <= pages; i++) {
      const li = document.createElement("li");
      li.className = "page-item";
      li.innerHTML = `<a href="#" class="page-link">${i}</a>`;
      li.addEventListener("click", e => {
        e.preventDefault();
        visible.forEach((r, j) => {
          r.style.display = (j >= (i - 1) * perPage && j < i * perPage) ? "" : "none";
        });
        document.querySelectorAll(".page-item").forEach(p => p.classList.remove("active"));
        li.classList.add("active");
      });
      paginationContainer.appendChild(li);
    }

    if (pages > 0) paginationContainer.firstChild.classList.add("active");
  }

  document.querySelectorAll(".openOffcanvasBtn").forEach(btn => {
    btn.addEventListener("click", () => {
      const leadId = btn.dataset.id;
      console.log("Opening offcanvas for leadId:", leadId);
      document.getElementById("leadId").value = leadId;

      fetch(`/lead_data_collection_hr/${leadId}/`)
        .then(res => res.json())
        .then(data => {
          console.log("Lead data fetched============:", data);
          console.log("🧪 Next follow-up from backend:", data.next_followup);
          if (data.success) {
            document.getElementById("leadName").textContent = data.lead.name;
            document.getElementById("leadEmail").textContent = data.lead.email;
            document.getElementById("leadPhone").textContent = data.lead.contact;
            document.getElementById("leadAddedDate").textContent = data.lead.added_date;
            document.getElementById("clientName").textContent = data.client.name;
            document.getElementById("clientBusiness").textContent = data.client.business;
            document.getElementById("telecallerName").textContent = data.telecaller.name;
            document.getElementById("collectedByName").textContent = data.collected_by.name;
            document.getElementById("clientCategory").textContent = data.category || "-";
            document.getElementById("collectedCategory").textContent = data.category || "-";
            document.getElementById("currentStatus").textContent = data.current_status || "-";
            document.getElementById("nextFollowDateDisplay").textContent = data.next_followup || "-";

            offcanvas.show();

            fetch(`/get-followup-data/${leadId}/`)
              .then(res => res.json())
              .then(extra => {
                console.log("Follow-up extra fetched:", extra);
                if (extra.success) {
                  document.getElementById("followupDetailsContent").innerHTML = extra.details.map(d =>
                    `<div class="mb-2">
                      <h6>${d.telecaller}</h6>
                      <p><strong>Date:</strong> ${d.date}</p>
                      <p><strong>Response:</strong> ${d.response}</p>
                      <p><strong>Next Follow Up:</strong> ${d.next}</p>
                      <p><strong>Status:</strong> ${d.status}</p>
                      <hr>
                    </div>`).join("");

                  document.getElementById("followupHistoryContent").innerHTML = extra.history.map(h =>
                    `<div class="mb-2">
                      <h6>${h.client}</h6>
                      <p><strong>Date:</strong> ${h.date}</p>
                      <p><strong>Allocated to:</strong> ${h.telecaller}</p>
                      <p><strong>Note:</strong> ${h.note}</p>
                      <p><strong>Status:</strong> <strong>${h.status}</strong></p>
                      <hr>
                    </div>`).join("");

                  document.getElementById("recordingsContent").innerHTML = extra.recordings.map(r =>
                    `<div class="mb-3">
                      <p><strong>Date:</strong> ${r.date}</p>
                      <audio controls src="${r.url}" class="w-100"></audio>
                    </div>`).join("");
                }
              })
              .catch(err => console.error("Follow-up data fetch error:", err));
          } else {
            console.warn("Failed to load lead data:", data.message);
            alert("Failed to load lead data.");
          }
        })
        .catch(error => {
          console.error("Fetch error:", error);
          alert("An error occurred while loading lead data.");
        });
    });
  });


const wasteModal = new bootstrap.Modal(document.getElementById("wasteModal"));

document.getElementById("markWasteBtn").addEventListener("click", () => {
  const leadId = document.getElementById("leadId").value;
  console.log("Waste status triggered for lead:", leadId);
  document.getElementById("wasteReason").value = "";
  wasteModal.show();
});

document.getElementById("confirmWasteBtn").addEventListener("click", () => {
  const leadId = document.getElementById("leadId").value;
  const reason = document.getElementById("wasteReason").value.trim();

  if (!reason) {
    alert("Please provide a reason.");
    return;
  }

  fetch("/update-lead-status/", {
    method: "POST",
    headers: {
      "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      lead_id: leadId,
      status: "Waste Lead",
      reason: reason
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Lead marked as waste.");
        location.reload();
      } else {
        alert("Failed to update status.");
      }
    });

  wasteModal.hide();
});


  // Status change buttons
  document.getElementById("btnLeadJoined").addEventListener("click", () => {
    const leadId = document.getElementById("leadId").value;
    console.log("Status Change: Lead Joined", leadId);
    updateLeadStatus(leadId, "Lead Joined");
  });

  document.getElementById("btnLeadClosed").addEventListener("click", () => {
    const leadId = document.getElementById("leadId").value;
    console.log("Status Change: Lead Closed", leadId);
    updateLeadStatus(leadId, "Lead Closed");
  });



  function updateLeadStatus(leadId, status, reason = "") {
    const formData = new FormData();
    formData.append("lead_id", leadId);
    formData.append("status", status);
    if (reason) formData.append("reason", reason);

    fetch("/update-lead-status/", {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert("Lead status updated.");
          location.reload();
        } else {
          alert("Failed to update status.");
        }
      })
      .catch(err => {
        console.error("Status update error:", err);
        alert("An error occurred while updating status.");
      });
  }

  document.getElementById("followupForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    for (const [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
    }

    fetch("/submit-followup-update/", {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert("Follow-up updated.");
          location.reload();
        } else {
          alert("Update failed.");
        }
      });
  });

  searchInput.addEventListener("input", filterTable);
  statusFilter.addEventListener("change", filterTable);
  fromDate.addEventListener("change", filterTable);
  toDate.addEventListener("change", filterTable);
  nextFollowUpDate.addEventListener("change", filterTable);
  rowCount.addEventListener("change", paginate);
  document.getElementById("clearFilters").addEventListener("click", () => location.reload());

  document.getElementById("clearSearch").addEventListener("click", () => {
    location.reload()
  });


  filterTable();
});
