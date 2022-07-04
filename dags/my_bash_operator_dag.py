from datetime import timedelta
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
default_args = {
    'owner': 'giang',
    'retries': 5,
    'retry_deplay': timedelta(minutes=2)

}

with DAG(
    dag_id= 'my_bash_operator_dag',
    description= 'This is my first bash operator dag',
    start_date=datetime(2022,1,7),
    schedule_interval=  '@daily' 
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello world, this is a first task'
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo this is a second task'
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo this is a third task'
    )

    #task1.set_downstream([task2, task3])

    task1 >> [task2, task3]


