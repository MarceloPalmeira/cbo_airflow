from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import psycopg2
import os

def load_json_to_postgres():
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cbo_subgrupo_principal (
            code VARCHAR PRIMARY KEY,
            name TEXT
        );
    """)

    path = "/opt/airflow/data/CBO2002 - SubGrupo Principal.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        cur.execute("""
            INSERT INTO cbo_subgrupo_principal (code, name)
            VALUES (%s, %s)
            ON CONFLICT (code) DO NOTHING;
        """, (item["code"], item["name"]))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="load_cbo_subgrupo_principal",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    task = PythonOperator(
        task_id="load_json_to_postgres",
        python_callable=load_json_to_postgres
    )
