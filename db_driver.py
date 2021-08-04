import pandas as pd
from constants import *

raw_data = {'task_name': ['buy beer', 'do stuff', 'be happy', 'get rich'],
            'completed': [True, False, True, False]}

df = pd.DataFrame(raw_data)


def locate_task(task_name):
    return task_name in set(df['task_name'])


def delete_task_from_df(task_name):
    global df
    df = df.drop(df.index[df[TASK_NAME] == task_name])


def add_new_task(data):
    global df
    df = pd.DataFrame.append(df, data, ignore_index=True)


def task_is_completed(task_name):
    global df
    idx = df.index[df[TASK_NAME] == task_name]
    return list(df.loc[idx]['completed'])[0]


def set_task_as_completed(task_name):
    idx = df.index[df[TASK_NAME] == task_name]
    df.loc[idx] = task_name, True


def set_task_new_state(task_name):
    idx = df.index[df[TASK_NAME] == task_name]
    # set the opposite value
    df.loc[idx] = task_name, not list(df.loc[idx][TASK_COMPLETED])[0]
    return TASK_CHANGE_STATE


def task_state_already_set(task_name, current_state):
    global df
    value_of_task = True if current_state == COMPLETE_TASK else False
    idx = df.index[df[TASK_NAME] == task_name]
    return list(df.loc[idx][TASK_COMPLETED])[0] == value_of_task


def update_task(old_task, updated_task):
    global df
    idx = df.index[df[TASK_NAME] == old_task]
    df.loc[idx] = updated_task, False
    return UPDATED_TASK


def get_list_of_tasks(feature):
    global df

    list_of_tasks = df.to_dict(orient="split")["data"]
    return generate_task_table(list_of_tasks,feature)


def build_table_of_tasks(tasks_list, feature):
    task_str = ""
    for task in tasks_list:
        completed = '+' if task[1] is True else '-'
        spaces = " " * (SPACE_FACTOR - len(task[0]))
        line = task[0] + spaces + completed + "\n"
        task_str += line
    return task_str


def generate_task_table(tasks_list, feature):
    msg = NO_TASKS
    if feature == LIST_COMPLETED_TASKS:
        tasks_list = list(filter(lambda x: x[1], tasks_list))
        msg = NO_COMPLETED_TASKS
    if len(tasks_list) == 0:
        return msg
    else:
        tasks = build_table_of_tasks(tasks_list, feature)
        print(tasks)
        return tasks

