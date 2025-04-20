import os
import boto3
import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def upload_to_minio(file_path: str, bucket: str, key: str, **kwargs):
    """
    Sube un archivo local a un bucket de MinIO/S3.
    """
    endpoint_url = os.getenv("AWS_ENDPOINT_URL_S3")
    client = boto3.client("s3", endpoint_url=endpoint_url)
    logging.info(f"Subiendo {file_path} al bucket {bucket} con key {key} usando endpoint {endpoint_url}")
    client.upload_file(file_path, bucket, key)
    logging.info("Subida completada")

with DAG(
    dag_id="etl_wine_to_minio",
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=["etl", "wine"],
) as dag:

    load_local_to_minio = PythonOperator(
        task_id="upload_csv",
        python_callable=upload_to_minio,
        op_kwargs={
            "file_path": "/opt/airflow/data/wine_profiles6.csv",
            "bucket": "data",
            "key": "raw/wine_profiles6.csv",
        },
    )

