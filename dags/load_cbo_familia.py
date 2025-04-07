from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import psycopg2

def load_data():
    conn = psycopg2.connect(host="postgres", database="airflow", user="airflow", password="airflow")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cbo_familia (code VARCHAR PRIMARY KEY, name TEXT);""")
    with open("/opt/airflow/data/CBO2002 - Familia.json", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        cur.execute("""INSERT INTO cbo_familia (code, name) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING;""", (item["code"], item["name"]))
    conn.commit()
    cur.close()
    conn.close()

with DAG(dag_id="load_cbo_familia", start_date=datetime(2023, 1, 1), schedule_interval=None, catchup=False) as dag:
    task = PythonOperator(task_id="load_cbo_familia_task", python_callable=load_data)