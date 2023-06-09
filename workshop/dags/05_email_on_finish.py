from airflow import DAG  
from airflow.operators.bash import BashOperator 
from datetime import datetime, date, timedelta
from airflow.utils.dates import days_ago

from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.operators.email_operator import EmailOperator

from google.cloud import storage
import os

default_args = {
    'owner': 'ADMIN',
    'start_date': days_ago(6)  # date.today(); days_ago(6) datetime(2022, 12, 1)
}

dag_args = {
    'dag_id': '05-email-on-finish',
    'schedule_interval': '@monthly',
    'catchup': False,
    'default_args': default_args,
    "doc_md":(
    """
    # 05-email-on-finish

    ## DAG PARA COMPROBAR SI EL CSV EXISTE EN LA RUTA DADA

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

    ##### TAREA load_data_to_big_query
    dataset_table =  "airflow-388217.external_data.enquestes"
    load_data_to_big_query = GCSToBigQueryOperator(
        task_id='load_data_to_big_query',
        bucket=bucket_name,
        source_objects=[destination_file_path], # Todos los elementos del bucket
        source_format='CSV', # Formato de los archivos a insertar
        skip_leading_rows=1, # No considerar la primera fila como datos porque la primera fila son las cabeceras
        field_delimiter=',', # Delimitador
        destination_project_dataset_table=dataset_table, # id de la tabla + el nombre
        create_disposition='CREATE_IF_NEEDED', # Crearla si no existe
        write_disposition='WRITE_APPEND', # Añade a los datos existentes
        bigquery_conn_id='google_cloud_default', # Valor por defecto
        google_cloud_storage_conn_id='google_cloud_default' # Valor por defecto
    )

    ##### TAREA load_filtered_data_to_big_query

    query = f'''SELECT * FROM `{dataset_table}` WHERE NOM_DISTRICTE='EIXAMPLE' LIMIT 1000'''
    dataset_table_eixample = "airflow-388217.external_data.enquestes_eixample"
    create_table_exiample = BigQueryExecuteQueryOperator(
        task_id='create_table_exiample',
        sql=query,
        destination_dataset_table=dataset_table_eixample,
        write_disposition='WRITE_TRUNCATE', # Eliminar los datos antes de volver a escribir
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        #bigquery_conn_id='google_cloud_default'
    )

    # TAREA  success_email
    dest_email = ['fpa@nextret.net']
    success_email = EmailOperator(
        task_id='send_email',
        to=dest_email,
        subject='La ejecución del dag ' + dag_args['dag_id'] +' correcta', # Asunto
        html_content=f'''<h3>ÉXITO EN LA EJECUCIÓN!!</h3> <p>La ejecución del dag {dag_args['dag_id']} ha acabado correctamente :)</p> ''', # Contenido
        dag=dag
    )
    
    (check_file_task >> 
    upload_csv_to_gcs >> 
    load_data_to_big_query >> 
    create_table_exiample >> success_email)

