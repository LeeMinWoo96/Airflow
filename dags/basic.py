
import os
import sys

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

"""
depends_on_past: when set to True, keeps a task from getting triggered if the previous schedule for the task hasn’t succeeded

wait_fow_downstream: when set to true, an instance of task X will wait for tasks immediately downstream of the previous instance of task X to finish successfully before it runs.

retries (int) – the number of retries that should be performed before failing the task

catchup - backfill 할건지 

"""

default_args = {
        
        'owner' : 'airflow',
        'depends_on_past' : True,
        'wait_for_downstream' : True,
        'start_date' : datetime(2020,2,12),
        'schedule_interval': '@once'
        }


def printff(**kwargs):
    print("Hi")



dag = DAG(
        dag_id = 'testing',
        catchup = True,
        default_args = default_args,
        )



dummy = DummyOperator(
        task_id = 'dummy',
        dag = dag)


tt = PythonOperator(
        task_id = 'tt',
        python_callable = printff,
        dag= dag)


tt.set_upstream(dummy)






