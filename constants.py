ADD_TASK = "add-task"
UPDATE_TASK = "update-task"
LIST_TASKS = "list-tasks"
COMPLETE_TASK = "complete-task"
UNDO_TASK = "undo-task"
DELETE_TASK = "delete-task"
LIST_COMPLETED_TASKS = "list-completed-tasks"

SPACE_FACTOR = 30

TASK_NOT_FOUND = 'task not found'
TASK_FOUND = 'task found'
TASK_STATUS = 'task_status'
TASK_ADDED = "task added"
TASK_EXIST = "task already exists!"
OLD_TASK = "old_task"
UPDATED_TASK = "updated_task"
NO_TASKS = "no tasks"
SUCCESS = "success"
TASK_NAME = "task_name"
TASK_COMPLETED = "completed"
TASK_ALREADY_IN_STATE = "task already in this state"
TASK_CHANGE_STATE = "task state is now changed"
TASK_DELETED = "task is now deleted"
NO_COMPLETED_TASKS = "no completed tasks exist"


# URLS
URL = "http://localhost:8080"
GET_TASK_ROUTE = '/getTask'
ADD_TASK_ROUTE = "/addTask"
UPDATE_TASK_ROUTE = "/updateTask"
GET_LIST_ROUTE = "/getListOfTasks"
COMPLETE_TASK_ROUTE = "/completeTask"
CHANGE_TASK_STATE_ROUTE = "/changeState"
DELETE_TASK_ROUTE = "/deleteTask"
GET_TASK_URL_COMMAND = URL + GET_TASK_ROUTE + "?task="
ADD_TASK_URL = URL + ADD_TASK_ROUTE
UPDATE_TASK_URL = URL + UPDATE_TASK_ROUTE
GET_LIST_TASKS = URL + GET_LIST_ROUTE
COMPLETE_TASK_URL = URL + COMPLETE_TASK_ROUTE
CHANGE_TASK_STATE_URL = URL + CHANGE_TASK_STATE_ROUTE
DELETE_TASK_URL = URL + DELETE_TASK_ROUTE


# SERVER

HOST_NAME = "localhost"
SERVER_PORT = 8080
STATUS_SUCCESS = 200
