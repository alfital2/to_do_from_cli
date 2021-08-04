import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from db_driver import *


class MyServer(BaseHTTPRequestHandler):

    def get_route(self, address):
        return address.split("?")[0]

    def do_GET(self):
        route = self.get_route(self.path)  # TO-DO make function
        get_req_data = parse_qs(urlparse(self.path).query)
        if route == GET_TASK_ROUTE:
            self.get_task_route(get_req_data)
        elif route == GET_LIST_ROUTE:
            self.get_list_of_all_tasks(get_req_data)

    def do_POST(self):
        route = self.get_route(self.path)  # TO-DO make function
        if route == ADD_TASK_ROUTE:
            self.add_new_task()
        elif route == UPDATE_TASK_ROUTE:
            self.update_task()
        elif route == CHANGE_TASK_STATE_ROUTE:
            self.update_task_state()
        elif route == DELETE_TASK_ROUTE:
            self.delete_task()

    def delete_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = (self.rfile.read(content_length)).decode("utf-8")
        if not locate_task(post_data):
            res = {ERROR: TASK_NOT_FOUND}
        else:
            delete_task_from_df(post_data)
            res = {TASK_STATUS: TASK_DELETED}
        self._set_response(json.dumps(res), STATUS_SUCCESS)

    def update_task_state(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads((self.rfile.read(content_length)).decode("utf-8"))
        print(post_data)
        if not locate_task(post_data[TASK_NAME]):
            res = {ERROR: TASK_NOT_FOUND}
        elif task_state_already_set(post_data[TASK_NAME], post_data[TASK_STATUS]):
            state = TASK_COMPLETED if post_data[TASK_STATUS] == COMPLETE_TASK else TASK_ACTIVE
            res = {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + state}
        else:
            res = {TASK_STATUS: set_task_new_state(post_data[TASK_NAME])}
        self._set_response(json.dumps(res), STATUS_SUCCESS)

    def _set_response(self, json_str, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json_str.encode('utf-8'))

    def get_task_route(self, get_req_data):
        task_found = locate_task(get_req_data['task'][0])
        if task_found:
            res = {TASK_STATUS: TASK_FOUND}
            self._set_response(json.dumps(res), STATUS_SUCCESS)
        else:
            res = {TASK_STATUS: TASK_NOT_FOUND}
            self._set_response(json.dumps(res), STATUS_SUCCESS)

    def get_list_of_all_tasks(self, function):
        res = get_list_of_tasks(function['function'][0])
        self._set_response(json.dumps({"out": res}), STATUS_SUCCESS)

    def add_new_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = (self.rfile.read(content_length)).decode("utf-8")
        if locate_task(post_data):
            res = {ERROR: TASK_EXIST}
        else:
            add_new_task({TASK_NAME: post_data, TASK_COMPLETED: False})
            res = {SUCCESS: TASK_ADDED}
        self._set_response(json.dumps(res), STATUS_SUCCESS)

    def update_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads((self.rfile.read(content_length)).decode("utf-8"))
        if not locate_task(post_data[OLD_TASK]):
            res = {ERROR: TASK_NOT_FOUND}
        elif task_is_completed(post_data[OLD_TASK]):
            res = {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + TASK_COMPLETED}
        else:
            res = {SUCCESS: update_task(post_data[OLD_TASK], post_data[UPDATED_TASK])}
        self._set_response(json.dumps(res), STATUS_SUCCESS)


if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
