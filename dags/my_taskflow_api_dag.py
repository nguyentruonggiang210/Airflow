from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'giang',
    'retries': 5,
    'retry_deplay': timedelta(minutes=5)
}


@dag(dag_id='dag_with_taskflow_api',
    default_args=default_args,
    start_date=datetime(2022, 7, 1),
    schedule_interval='@daily')
def hello_world_etl():
    
    @task()
    def get_name():
        return 'Giang'

    @task()
    def get_age():
        return 22

    @task()
    def greet(name, age):
        print(f'My name is {name}. Im {age} years old')

    @task(multiple_output=True)
    def set_multiple_name(greet):
        return {
            'first_name': 'nguyen',
            'middle_name': 'truong',
            'last_name': 'giang',
        }
    
    @task()
    def get_multiple_name(first_name, middle_name, last_name):
        return f"""
            First Name: {first_name}
            Middle Name: {middle_name}
            Last Name: {last_name}
        """

    name = get_name()
    age = get_age()
    greet(name=name, age=age) >> set_multiple_name()
    name_dict = set_multiple_name()
    get_multiple_name(name_dict['first_name'], name_dict['middle_name'], name_dict['last_name'])

greet_dag = hello_world_etl()