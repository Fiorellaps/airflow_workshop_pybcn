from airflow import DAG  
from airflow.operators.bash import BashOperator 
from datetime import datetime, date
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

from google.cloud import storage
import os

default_args = {
    'owner': 'ADMIN',
    'start_date': days_ago(6)  # date.today(); days_ago(6) datetime(2022, 12, 1)
}

dag_args = {
    'dag_id': '03-load-data-to-big-query',
    'schedule_interval': '@monthly',
    'catchup': False,
    'default_args': default_args,
    "doc_md":(
    """
    # 03-load-data-to-big-query

    Añadir datos almacenados en Google Cloud Storage a Big Query.

    """),
}

def upload_csv_to_gcs(file_path, bucket_name, destination_file_path):
    # Set the path to the credentials JSON file
    credentials_path = Variable.get("gcp_credentials_path") 

    # Set the environment variable with the path to the credentials file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    # Create a client using the credentials
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_file_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {bucket_name}/{destination_file_path}")
	

with DAG(**dag_args) as dag:

    ##### TAREA check_file_task
    # Create abslotue path to file and bash script
    #base_dag_path = "/root/airflow/dags"
    base_dag_path = Variable.get("base_dag_path")  
  
    file_path = "external_data/*.csv"
    absolute_file_path = os.path.join(base_dag_path, file_path)
    
    bash_file_path = "utiles/check_file.sh"
    absolute_bash_file_path = os.path.join(base_dag_path, bash_file_path)
 
    check_file_task = BashOperator(
        task_id='check_file',
        bash_command='sh ' + absolute_bash_file_path  + ' ' + absolute_file_path 
    )

    check_file_task.doc_md = ("""
    ## Bash Operator
    comprueba si un fichero existe
    """)

    ##### TAREA upload_csv_to_gcs
    destination_file_path = "external_data/serveis_municipals_evolucio_2022.csv"
    absolute_file_path = "/root/airflow_old/dags/external_data/serveis_municipals_evolucio_2022.csv"
    # TO DO; PROBAR SIN PASARLE EL NOMBRE DEL FICHERO
    bucket_name = "dades_enquestes"
    upload_csv_to_gcs = PythonOperator(
        task_id='upload_csv_to_gcs',
        python_callable=upload_csv_to_gcs,
        #op_args=[absolute_file_path, bucket_name, destination_file_path]
        op_kwargs={ 
            'file_path': absolute_file_path,
            'bucket_name': bucket_name,
            'destination_file_path': destination_file_path
         }   
    )

    upload_csv_to_gcs.doc_md = ("""
    ## Python Operator
    Sube un fichero a Google Cloud Storage
    """)

    ##### TAREA upload_csv_to_gcs

    load_data_to_big_query = GCSToBigQueryOperator(
        task_id='load_data_to_big_query',
        bucket=bucket_name, # Bucket a consultar
        source_objects=[destination_file_path], # Todos los elementos del bucket desde el que vamos a coger los datos
        source_format='CSV', # Formato de los archivos a insertar
        skip_leading_rows=1, # No considerar la primera fila como datos porque la primera fila son las cabeceras
        field_delimiter=',', # Delimitador
        destination_project_dataset_table='airflow-388217.external_data.enquestes', # id de la tabla + el nombre
        create_disposition='CREATE_IF_NEEDED', # Crearla si no existe
        write_disposition='WRITE_APPEND', # Añade a los datos existentes
        bigquery_conn_id='google_cloud_default', # Valor por defecto
        google_cloud_storage_conn_id='google_cloud_default' # Valor por defecto
    )
    
    check_file_task >> upload_csv_to_gcs >> load_data_to_big_query

