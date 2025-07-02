from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
import sys
import os

# Add /opt/airflow/config to Python path so it can find the "scripts" package
sys.path.append('/opt/airflow/airflow')

# Import from the scripts module
from config.scripts.pipeline_utils import (
    extract_commoncrawl,
    extract_abr_zip,
    match_with_gemini,
    insert_to_postgres
)

# Default arguments (optional but useful)
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'execution_timeout': timedelta(minutes=120)
}

# Define the DAG
with DAG(
    dag_id='company_data_etl',
    default_args=default_args,
    start_date=datetime(2025, 7, 1),
    schedule ='@daily',
    catchup=False,
    description='ETL pipeline for processing company data'
) as dag:

    task1 = PythonOperator(
        task_id='extract_commoncrawl',
        python_callable=extract_commoncrawl
    )

    task2 = PythonOperator(
        task_id='extract_abr',
        python_callable=extract_abr_zip
    )

    task3 = PythonOperator(
        task_id='gemini_match',
        python_callable=match_with_gemini
    )

    task4 = PythonOperator(
        task_id='insert_to_postgres',
        python_callable=insert_to_postgres
    )

    # Set task dependencies
    task1 >> task2 >> task3 >> task4
