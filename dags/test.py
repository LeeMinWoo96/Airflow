
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



# path 가 이 디렉토리가 아니라 tmp 에 있음 절대경로나 다른 방법으로 지정해줘야함 


sh_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/shell/'

#def printff(**kwargs):
#    sh_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/shell/'
#    print(sh_path)



dag = DAG(
        dag_id = 'testing_aws',
        catchup = True,
        default_args = default_args,
        )


# 반드시 뒤에 공백 넣어야함 안그러면 jinja와 충돌
task1_command = 'sh ' + sh_path + 'run_aws_load_mc100.sh '
task2_command = 'sh ' + sh_path + 'run_inference.sh '


dummy = DummyOperator(
        task_id = 'dummy',
        dag = dag)



t1 = BashOperator(
        task_id = 'load_mc100_task',
        bash_command = task1_command,
        dag=dag)


t2 = BashOperator(
        task_id = 'inference_task',
        bash_command = task2_command,
        dag=dag)

#tt = PythonOperator(
#        task_id = 'tt',
#        python_callable = printff,
#        dag= dag)



t1.set_upstream(dummy)
t2.set_upstream(t1)





