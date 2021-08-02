import json

import pandas as pd

from constants import *

raw_data = {'task_name': ['buy beer', 'fart', 'be happy', 'get rich'],
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


def task_state_already_set(task_name, current_state):
    global df
    value_of_task = True if current_state == COMPLETE_TASK else False
    idx = df.index[df[TASK_NAME] == task_name]
    return list(df.loc[idx][TASK_COMPLETED])[0] == value_of_task


def update_task(old_task, updated_task):
    global df
    if task_is_completed(old_task):
        return {TASK_STATUS: TASK_ALREADY_IN_STATE + ":" + TASK_COMPLETED}
    idx = df.index[df[TASK_NAME] == old_task]
    df.loc[idx] = updated_task, False
    return {TASK_STATUS: UPDATED_TASK}


def get_list_of_tasks():
    res = df.to_json(orient="split")
    parsed = json.loads(res)
    return parsed


update_task('buy beer', 'fart')
