from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pipeline import run_pipeline, process_and_save_results
import logging
data_file_path = 'UIM_data.csv'
dict_file_path = 'UIM_dictionary.xlsx'

# Define DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('my_dag', default_args=default_args, schedule_interval=timedelta(days=1))

# Define tasks
def run_and_save_results(**kwargs):
    results = run_pipeline(data_file_path, dict_file_path)
    output_path = process_and_save_results(results)
    return output_path

run_and_save_results_task = PythonOperator(
    task_id='run_and_save_results',
    python_callable=run_and_save_results,
    provide_context=True,  # Pass context to the callable function
    dag=dag,
)

# Set up task dependencies
run_and_save_results_task  # No dependencies for this task as it's the starting point

# Your next steps/tasks go here...

# Example: Data transformation process
def data_transformation(**kwargs):
    output_path = kwargs['output_path']
    logging.info(f"CSV file saved at: {output_path}")
    # Your data transformation logic goes here
    logging.info("Data transformation step")

data_transformation_task = PythonOperator(
    task_id='data_transformation',
    python_callable=data_transformation,
    provide_context=True,
    op_kwargs={'output_path': '{{ task_instance.xcom_pull(task_ids="run_and_save_results") }}'},
    dag=dag,
)

# Set up task dependencies
run_and_save_results_task >> data_transformation_task  # Now, data_transformation_task runs after run_and_save_results_task
