from os.path import isfile
from sqlite3 import connect
from dotenv import dotenv_values
import os

from apscheduler.triggers.cron import CronTrigger

config = dotenv_values(".env")

DB_PATH = config["DB_PATH"]
BUILD_PATH = config["BUILD_PATH"]

# print(os.path.join(os.getcwd(), DB_PATH))

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def commit():
    cxn.commit()


def close():
    cxn.close()


def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))


def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    cur.executemany(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())