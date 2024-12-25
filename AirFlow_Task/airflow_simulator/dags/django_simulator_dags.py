import os
import django
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add your Django project directory to Python path
sys.path.append('/mnt/d/Giza/GIZA_TASKS/AirFlow_Task/airflow_simulator')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airflow_simulator.settings')
django.setup()

from simulator.models import Simulator

def call_kpi_endpoint(kpi_id, **kwargs):
    """Task function to call the KPI endpoint."""
    import requests
    import random

    # Generate a random value
    random_value = random.uniform(1.0, 100.0)

    # Call the KPI endpoint
    response = requests.get(
        f"http://127.0.0.1:8000/simulator/kpi/",  # Update this URL if Django runs elsewhere
        params={"value": random_value},
    )

    # Log the response
    print(f"KPI Response for ID {kpi_id}: {response.json()}")

# Dynamically generate DAGs for each Simulator instance
for simulator in Simulator.objects.all():
    # Default arguments for the DAG
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    # Define the DAG
    dag = DAG(
        dag_id=f"simulator_dag_{simulator.id}",  # Unique DAG ID
        default_args=default_args,
        description=f"DAG for Simulator {simulator.id}",
        schedule_interval=simulator.interval,
        start_date=simulator.start_date,
        catchup=False,  # Do not backfill DAG runs
    )

    # Define the PythonOperator task
    task = PythonOperator(
        task_id=f"task_simulator_{simulator.id}",
        python_callable=call_kpi_endpoint,
        op_kwargs={'kpi_id': simulator.kpi_id},
        dag=dag,
    )

    # Register the DAG in globals()
    globals()[f"simulator_dag_{simulator.id}"] = dag
