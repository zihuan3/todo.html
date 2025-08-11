// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    const addTaskForm = document.getElementById('add-task-form');
    const taskInput = document.getElementById('task-input');
    const tasksContainer = document.getElementById('tasks-container');
    const completedTasksContainer = document.getElementById('completed-tasks-container');

    // Add task functionality
    addTaskForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent page refresh

        const taskText = taskInput.value.trim();
        if (!taskText) {
            alert('Please enter a task!');
            return;
        }

        // Send POST request to add task
        fetch('/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `task=${encodeURIComponent(taskText)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addTaskToDOM(taskText, data.index);
                taskInput.value = ''; // Clear input
                removeEmptyState();
            } else {
                alert('Error adding task: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding task. Please try again.');
        });
    });

    // Handle task actions (complete, edit, delete)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('task-checkbox')) {
            completeTask(e.target);
        } else if (e.target.classList.contains('delete-btn')) {
            deleteTask(e.target);
        } else if (e.target.classList.contains('edit-btn')) {
            editTask(e.target);
        }
    });

    // Complete task function
    function completeTask(checkbox) {
        const taskIndex = checkbox.getAttribute('data-task-index');
        const taskItem = checkbox.closest('.task-item');

        fetch(`/complete/${taskIndex}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Move task to completed section
                moveTaskToCompleted(taskItem, data.task_text);
                updateTaskIndices();
            } else {
                checkbox.checked = false; // Revert checkbox
                alert('Error completing task: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            checkbox.checked = false; // Revert checkbox
            alert('Error completing task. Please try again.');
        });
    }

    // Delete task function
    function deleteTask(deleteBtn) {
        const taskIndex = deleteBtn.getAttribute('data-task-index');
        const completedIndex = deleteBtn.getAttribute('data-completed-index');
        const taskItem = deleteBtn.closest('.task-item');

        if (!confirm('Are you sure you want to delete this task?')) {
            return;
        }

        let url;
        if (taskIndex !== null) {
            url = `/delete/${taskIndex}`;
        } else if (completedIndex !== null) {
            url = `/delete_completed/${completedIndex}`;
        }

        fetch(url, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove task from DOM with animation
                taskItem.style.opacity = '0';
                taskItem.style.transform = 'translateX(-100%)';
                setTimeout(() => {
                    taskItem.remove();
                    updateTaskIndices();
                    checkForEmptyState();
                }, 300);
            } else {
                alert('Error deleting task: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting task. Please try again.');
        });
    }

    // Edit task function
    function editTask(editBtn) {
        const taskIndex = editBtn.getAttribute('data-task-index');
        const taskTextSpan = editBtn.closest('.task-item').querySelector('.task-text');
        const currentText = taskTextSpan.textContent;

        const newText = prompt('Edit task:', currentText);
        if (newText === null || newText.trim() === '' || newText.trim() === currentText) {
            return; // User cancelled or didn't change anything
        }

        fetch(`/edit/${taskIndex}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `task=${encodeURIComponent(newText.trim())}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                taskTextSpan.textContent = newText.trim();
                // Add a brief highlight effect
                taskTextSpan.style.backgroundColor = '#fff3cd';
                setTimeout(() => {
                    taskTextSpan.style.backgroundColor = '';
                }, 1000);
            } else {
                alert('Error editing task: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error editing task. Please try again.');
        });
    }

    // Add task to DOM
    function addTaskToDOM(taskText, taskIndex) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item fade-in';
        taskItem.setAttribute('data-index', taskIndex);

        taskItem.innerHTML = `
            <input type="checkbox" class="task-checkbox" data-task-index="${taskIndex}">
            <span class="task-text">${escapeHtml(taskText)}</span>
            <div class="task-actions">
                <button class="edit-btn" data-task-index="${taskIndex}">Edit</button>
                <button class="delete-btn" data-task-index="${taskIndex}">Delete</button>
            </div>
        `;

        tasksContainer.appendChild(taskItem);
    }

    // Move task to completed section
    function moveTaskToCompleted(taskItem, taskText) {
        // Create completed task element
        const completedTask = document.createElement('div');
        completedTask.className = 'task-item completed fade-in';

        // Get current number of completed tasks for indexing
        const completedCount = completedTasksContainer ? completedTasksContainer.children.length : 0;

        completedTask.innerHTML = `
            <input type="checkbox" class="task-checkbox" checked disabled>
            <span class="task-text">${escapeHtml(taskText)}</span>
            <div class="task-actions">
                <button class="delete-btn" data-completed-index="${completedCount}">Remove</button>
            </div>
        `;

        // Add to completed section
        if (!completedTasksContainer) {
            // Create completed section if it doesn't exist
            const completedSection = document.createElement('div');
            completedSection.innerHTML = '<h2 style="margin-top: 30px;">Completed Tasks:</h2>';
            const newCompletedContainer = document.createElement('div');
            newCompletedContainer.id = 'completed-tasks-container';
            completedSection.appendChild(newCompletedContainer);
            document.querySelector('.task-list').appendChild(completedSection);
            completedTasksContainer = newCompletedContainer;
        }

        completedTasksContainer.appendChild(completedTask);

        // Remove from active tasks with animation
        taskItem.style.opacity = '0';
        taskItem.style.transform = 'translateX(100%)';
        setTimeout(() => {
            taskItem.remove();
            checkForEmptyState();
        }, 300);
    }

    // Update task indices after deletion
    function updateTaskIndices() {
        const activeTasks = document.querySelectorAll('#tasks-container .task-item:not(.empty-state)');
        activeTasks.forEach((task, index) => {
            task.setAttribute('data-index', index);
            const checkbox = task.querySelector('.task-checkbox');
            const editBtn = task.querySelector('.edit-btn');
            const deleteBtn = task.querySelector('.delete-btn');

            if (checkbox) checkbox.setAttribute('data-task-index', index);
            if (editBtn) editBtn.setAttribute('data-task-index', index);
            if (deleteBtn) deleteBtn.setAttribute('data-task-index', index);
        });

        const completedTasks = document.querySelectorAll('#completed-tasks-container .task-item');
        completedTasks.forEach((task, index) => {
            const deleteBtn = task.querySelector('.delete-btn');
            if (deleteBtn) deleteBtn.setAttribute('data-completed-index', index);
        });
    }

    // Check if we need to show empty state
    function checkForEmptyState() {
        const activeTasks = document.querySelectorAll('#tasks-container .task-item:not(.empty-state)');
        if (activeTasks.length === 0) {
            showEmptyState();
        }
    }

    // Show empty state
    function showEmptyState() {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = '<p>No tasks yet. Add one above to get started!</p>';
        tasksContainer.appendChild(emptyState);
    }

    // Remove empty state
    function removeEmptyState() {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});