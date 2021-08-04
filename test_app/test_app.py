import ast
import json
import unittest
import requests
from constants import *

TASK_TEST_NAME = "test"
TASK_NEW_TEST_NAME = "new_name"


def clear_db():
    requests.post(DELETE_TASK_URL, data="test".encode('utf-8'))
    requests.post(DELETE_TASK_URL, data="new_name".encode('utf-8'))


def add_task(name):
    task = name
    requests.post(ADD_TASK_URL, data=task.encode('utf-8'))


class TestAppTest(unittest.TestCase):
    def test_add_task(self):
        # clear DB
        clear_db()
        expected = {SUCCESS: TASK_ADDED}
        response = requests.post(ADD_TASK_URL, data="test".encode('utf-8'))
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_add_task_that_exist(self):
        requests.post(ADD_TASK_URL, data="test".encode('utf-8'))
        response = requests.post(ADD_TASK_URL, data="test".encode('utf-8'))
        expected = {ERROR: TASK_EXIST}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_update_test(self):
        clear_db()
        old_task = "test"
        updated_task = "new_name"
        requests.post(ADD_TASK_URL, data=old_task.encode('utf-8'))
        tasks_data = {OLD_TASK: old_task, UPDATED_TASK: updated_task}
        response = requests.post(UPDATE_TASK_URL, data=json.dumps(tasks_data))
        expected = {SUCCESS: UPDATED_TASK}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_update_non_exist(self):
        clear_db()
        old_task = "test"
        updated_task = "new_name"
        tasks_data = {OLD_TASK: old_task, UPDATED_TASK: updated_task}
        response = requests.post(UPDATE_TASK_URL, data=json.dumps(tasks_data))
        expected = {ERROR: TASK_NOT_FOUND}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_update_completed_task(self):
        clear_db()
        old_task = "test"
        updated_task = "new_name"
        requests.post(ADD_TASK_URL, data=old_task.encode('utf-8'))

        # update state
        completed = {TASK_NAME: old_task, TASK_STATUS: COMPLETE_TASK}
        requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))

        # update name
        tasks_data = {OLD_TASK: old_task, UPDATED_TASK: updated_task}
        response = requests.post(UPDATE_TASK_URL, data=json.dumps(tasks_data))
        expected = {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + TASK_COMPLETED}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_complete_task(self):
        clear_db()
        task = "test"
        requests.post(ADD_TASK_URL, data=task.encode('utf-8'))
        # update state
        completed = {TASK_NAME: task, TASK_STATUS: COMPLETE_TASK}
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))
        expected = {TASK_STATUS: TASK_CHANGE_STATE}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_complete_non_existing_task(self):
        clear_db()
        completed = {TASK_NAME: "someTest", TASK_STATUS: COMPLETE_TASK}
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))
        expected = {ERROR: TASK_NOT_FOUND}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_complete_completed_task(self):
        clear_db()
        task = "test"
        requests.post(ADD_TASK_URL, data=task.encode('utf-8'))

        # mark as completed
        completed = {TASK_NAME: task, TASK_STATUS: COMPLETE_TASK}
        requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))

        # mark AGAIN as completed
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))

        expected = {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + TASK_COMPLETED}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_undo_task(self):
        clear_db()
        task = "test"
        requests.post(ADD_TASK_URL, data=task.encode('utf-8'))
        # update state to complete
        completed = {TASK_NAME: task, TASK_STATUS: COMPLETE_TASK}
        requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))

        # update state to undo
        completed = {TASK_NAME: task, TASK_STATUS: UNDO_TASK}
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))

        expected = {TASK_STATUS: TASK_CHANGE_STATE}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_incomplete_task(self):
        clear_db()
        task = "test"
        requests.post(ADD_TASK_URL, data=task.encode('utf-8'))
        completed = {TASK_NAME: task, TASK_STATUS: UNDO_TASK}
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))
        expected = {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + TASK_ACTIVE}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_undo_non_existing_task(self):
        clear_db()
        completed = {TASK_NAME: "someTest", TASK_STATUS: COMPLETE_TASK}
        response = requests.post(CHANGE_TASK_STATE_URL, data=json.dumps(completed))
        expected = {ERROR: TASK_NOT_FOUND}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_delete_task(self):
        clear_db()
        add_task(TASK_TEST_NAME)
        response = requests.post(DELETE_TASK_URL, data=TASK_TEST_NAME.encode('utf-8'))
        expected = {TASK_STATUS: TASK_DELETED}
        self.assertEqual(ast.literal_eval(response.text), expected)

    def test_delete_non_existing_task(self):
        clear_db()
        response = requests.post(DELETE_TASK_URL, data=TASK_NEW_TEST_NAME.encode('utf-8'))
        expected = {ERROR: TASK_NOT_FOUND}
        self.assertEqual(ast.literal_eval(response.text), expected)


if __name__ == '__main__':
    unittest.main()
