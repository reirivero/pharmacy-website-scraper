# Import the libraries
from datetime import timedelta, datetime
# The DAG object; we'll need this to instatiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.python import PythonOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),# datetime(2023, 1, 1),
    'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='example dag',
    schedule_interval=timedelta(days=1),
)

# Define the tasks



# Task pipeline
