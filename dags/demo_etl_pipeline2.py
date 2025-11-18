from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Fonctions Python
def extract_data():
    """Extraction des données depuis une source"""
    print("🔍 Extraction des données...")
    data = {"users": 150, "orders": 450, "revenue": 25000}
    print(f"✅ Données extraites : {data}")
    return data

def transform_data(**context):
    """Transformation des données"""
    print("🔄 Transformation des données...")
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='extract')
    
    # Calculs
    data['avg_order_value'] = data['revenue'] / data['orders']
    print(f"✅ Données transformées : {data}")
    return data

def load_data(**context):
    """Chargement en base de données"""
    print("💾 Chargement en base de données...")
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='transform')
    print(f"✅ {len(data)} métriques chargées en DB")
    return True

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email': ['devsecopsdojo25@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='demo_etl_pipeline2',
    default_args=default_args,
    description='Pipeline ETL de démonstration',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo', 'etl', 'tutorial'],
) as dag:
    
    # Définition des tâches
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )
    
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )
    
    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )
    
    # Dépendances
    extract >> transform >> load