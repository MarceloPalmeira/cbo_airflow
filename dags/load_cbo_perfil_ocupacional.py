from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import psycopg2

def load_data():
    conn = psycopg2.connect(host="postgres", database="airflow", user="airflow", password="airflow")
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cbo_perfil_ocupacional (
            cod_grupo_grande VARCHAR,
            cod_subgrupo_principal VARCHAR,
            cod_subgrupo VARCHAR,
            cod_familia VARCHAR,
            cod_ocupacao VARCHAR,
            sgl_grande_area VARCHAR,
            nome_grande_area TEXT,
            cod_atividade VARCHAR,
            nome_atividade TEXT,
            PRIMARY KEY (cod_ocupacao, cod_atividade)
        );
    """)

    with open("/opt/airflow/data/CBO2002 - PerfilOcupacional.json", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        cur.execute("""
            INSERT INTO cbo_perfil_ocupacional (
                cod_grupo_grande, cod_subgrupo_principal, cod_subgrupo,
                cod_familia, cod_ocupacao, sgl_grande_area,
                nome_grande_area, cod_atividade, nome_atividade
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cod_ocupacao, cod_atividade) DO NOTHING;
        """, (
            item["cod_grupo_grande"],
            item["cod_subgrupo_principal"],
            item["cod_subgrupo"],
            item["cod_familia"],
            item["cod_ocupacao"],
            item["sgl_grande_area"],
            item["nome_grande_area"],
            item["cod_atividade"],
            item["nome_atividade"]
        ))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="load_cbo_perfil_ocupacional",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    task = PythonOperator(
        task_id="load_cbo_perfil_ocupacional_task",
        python_callable=load_data
    )
