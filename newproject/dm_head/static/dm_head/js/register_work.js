document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bars
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const value = parseInt(bar.dataset.progress) || 0;
        bar.style.width = value + '%';

        // if (value < 40) {
        //     bar.classList.add('bg-danger');
        // } else if (value < 70) {
        //     bar.classList.add('bg-warning');
        // } else {
            bar.classList.add('bg-success');
        // }
    });

    // Handle edit icons for tasks
    document.querySelectorAll('.edit-task-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const taskId = this.dataset.id;
            console.log('Edit task clicked:', taskId);
            // TODO: open edit modal or redirect
        });
    });

    // Handle delete icons for tasks
    document.querySelectorAll('.delete-task-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const taskId = this.dataset.id;
            if (confirm('Are you sure you want to delete this task?')) {
                console.log('Delete task confirmed:', taskId);
                // TODO: send delete request via AJAX or navigate to backend endpoint
            }
        });
    });

    // Handle main work edit buttons
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const workId = this.dataset.id;
            console.log('Edit work clicked:', workId);
            // TODO: open edit modal or redirect
        });
    });

    // Handle main work delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const workId = this.dataset.id;
            if (confirm('Are you sure you want to delete this work?')) {
                console.log('Delete work confirmed:', workId);
                // TODO: send delete request via AJAX or navigate to backend endpoint
            }
        });
    });

    // Handle add-task button
    document.querySelectorAll('.add-task-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const workId = this.dataset.id;
            console.log('Add task clicked for work ID:', workId);
            // TODO: open add task modal
        });
    });

    // Handle add-lead-category button
    document.querySelectorAll('.add-lead-category-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const workId = this.dataset.id;
            console.log('Add lead category clicked for work ID:', workId);
            // TODO: open add lead category modal
        });
    });

    // Handle add-fields button
    document.querySelectorAll('.add-fields-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const workId = this.dataset.id;
            console.log('Add fields clicked for work ID:', workId);
            // TODO: open add fields modal
        });
    });
});
