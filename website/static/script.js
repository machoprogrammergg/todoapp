function createNewTask() {
  window.location.href = "/new-task";
}

function deleteTask(taskId) {
  window.location.href = '/delete-task/' + taskId;
}


function markAsDone(taskId) {
  window.location.href = '/mark-as-done/' + taskId;
}