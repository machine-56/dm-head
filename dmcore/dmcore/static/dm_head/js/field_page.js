document.querySelectorAll('.add-field-category').forEach(btn => {
  btn.addEventListener('click', function () {
    const categoryId = this.dataset.categoryid;
    document.getElementById('addFieldForm').reset();
    document.getElementById('add_field_category_id').value = categoryId;

    fetch(`/get-category/${categoryId}/`)
      .then(res => res.json())
      .then(data => {
        document.getElementById('add_field_client').value = data.client_name;
        document.getElementById('add_field_category').value = data.collection_for;

        const modal = new bootstrap.Modal(document.getElementById('addFieldModal'));
        modal.show();
      });
  });
});

document.getElementById('addFieldForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const formData = new FormData(this);

  fetch('/add-field/', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    if (data.success) location.reload();
  });
});
document.getElementById('btnClearAddField').addEventListener('click', function () {
  document.querySelector('#addFieldForm input[name="field_name"]').value = '';
  document.querySelector('#addFieldForm textarea[name="description"]').value = '';
});
