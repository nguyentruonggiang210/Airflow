from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from sqlalchemy import false

# step 1: Create DAG

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'depends_on_past': False, # if last run succeed, work flow will not run
    'email': ['nguyentruonggiang210@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_deplay': timedelta(minutes=5), # if task's failed in workflow, it will retry after 5 minutes
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial of DAG',
    schedule_interval=timedelta(days=1) # can use cron expression
)

# step 2: Create task

t1 = BashOperator(
    task_id='print date',
    bash_command='date',
    dag = dag
)

t1.doc_md = """
    ### Task Documentation
    This is task documentation
"""

dag.doc_md = __doc__

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    dag = dag
)

template_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=template_command,
    params={'my_param':'Parameter I passes in'},
    dag = dag
)

# t1.set_downstream(t2) # t2 depend on t1 or t1 >> t2
# t3.set_upstream(t1) # t3 depend on t1
# or can use
t1 >> [t2,t3]