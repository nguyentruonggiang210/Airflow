from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, task
from datetime import datetime, date
default_args = {
    'owner': 'giang',
    'retries': 5,
    'retry_deplay': timedelta(minutes=5)
}

def greet():
    print('hello world')

def middle_task(date, ti): # must be ti
    name = ti.xcom_pull(task_ids='get_name')
    print('{0} executed at {1}'.format(name,date))

def get_name():
    return 'giang'

def push_xcoms(ti):
    ti.xcom_push(key='first_name',value='nguyen')
    ti.xcom_push(key='middle_name',value='truong')
    ti.xcom_push(key='last_name',value='giang')

def get_name_after_push(ti):
    first_name = ti.xcom_pull(task_ids='push_xcoms', key='first_name')
    middle_name = ti.xcom_pull(task_ids='push_xcoms', key='middle_name')
    last_name = ti.xcom_pull(task_ids='push_xcoms', key='last_name')

    return f'''
        First Name: {first_name}
        Middle Name: {middle_name}
        Last Name: {last_name}
    '''

with DAG(
    default_args= default_args,
    dag_id='my_python_operator',
    description='Our first dag using python operator',
    start_date=datetime(2022,1,7),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id='middle_task',
        python_callable=middle_task,
        op_kwargs={'date': '2020-10-10'}
    )

    task3 = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )

    task4 = PythonOperator(
        task_id='push_xcoms',
        python_callable=push_xcoms
    )

    task5 = PythonOperator(
        task_id='pull_after_push_xcoms',
        python_callable=get_name_after_push
    )

    task3.set_downstream(task1)
    task1.set_downstream(task2)
    task2.set_downstream([task5, task4])
