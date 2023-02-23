# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Ramesh Sannareddy',
    'start_date': days_ago(0),
    'email': ['ramesh@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='Practice ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)


# define the tasks

# define the first task named extract
download = BashOperator(
    task_id='download',
    bash_command='wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"',
    dag=dag,
)    

# define the second task named extract
extract = BashOperator(
    task_id='extract',
    bash_command='cut -d"#" -f1,4 /web-server-access-log.txt > /home/project/airflow/dags/extracted-log.txt',
    dag=dag,
)

# define the third task named transform
transform = BashOperator(
    task_id='transform',
    bash_command= 'tr "[:lower:]" "[:upper:]" > /home/project/airflow/dags/transformed-log.txt',
    dag=dag,
)

# define the fourth task named load

load = BashOperator(
    task_id='load',
    bash_command='zip extracted-log.txt transformed-log.txt',
    dag=dag,
)


# task pipeline
download >> extract >> transform >> load


"""
Submit the DAG.

 cp  ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags

Task 10: Verify if the DAG is submitted.

airflow dags list

"""