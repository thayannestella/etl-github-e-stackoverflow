from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'etl_user',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_github_stackoverflow',
    default_args=default_args,
    description='ETL pipeline for GitHub and Stack Overflow data',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

extract_task = BashOperator(
    task_id='extract',
    bash_command='cd /d/SENAC/etl-github-e-stackoverflow && python etl/main_extract.py',
    dag=dag,
)

transform_task = BashOperator(
    task_id='transform',
    bash_command='cd /d/SENAC/etl-github-e-stackoverflow && python etl/main_transform.py',
    dag=dag,
)

gold_task = BashOperator(
    task_id='gold',
    bash_command='cd /d/SENAC/etl-github-e-stackoverflow && python etl/main_gold.py',
    dag=dag,
)

extract_task >> transform_task >> gold_task