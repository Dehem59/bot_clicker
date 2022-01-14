from __future__ import absolute_import

from celery import current_task, Task

from bot_clicker.celery import app

@app.task()
def test_task():
    print("celery test log")

    return True