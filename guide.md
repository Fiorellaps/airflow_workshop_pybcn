# Workshop de Airflow

# 1. Instalación de Airflow en Linux

- Creamos un entorno de Python con virtualenv y lo activamos


```python
!python -m venv airflow_env
>source airflow_env/bin/ativate
```

- Definimos **AIRFLOW_HOME**


```python
>export AIRFLOW_HOME=~/airflow
```

- Instalamos airflow desde Pypi


```python
!pip install "apache-airflow[gcp]"
```

<div style="color:green">Airflow ofrece muchos más <a href="https://airflow.apache.org/docs/#providers-packagesdocsapache-airflow-providersindexhtml">providers</a>.
</div>

- Modificar la configuración de airflow


```python
>nano /root/airflow/airflow.cfg
#- load_examples=False
#- sql_alchemy_conn = postgresql+psycopg2://user:pass@localhost:5432/airflow_db
```

- Comprobamos que está bien instalado


```python
airflow version
```

- Arrancamos airflow manualmente
<div style="color:green">** También se podría arrancar usando el comando `airflow standalone` o en modo cluster
</div>

# 2. Arrancar Airflow

## 1.1. Base de datos (Postgres, SQLite, etc.)


<div style="color:green">
** Más información en https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html
</div>

##### PREPARAR EL POSTGRES

<div style="color:orange">
    
    
- CREATE DATABASE airflow_db;

- CREATE USER airflow_user WITH PASSWORD 'XXX';
    
- GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
    
- ALTER ROLE airflow_user SET search_path = public;    
   
    
</div>

##### INICIALIZAR POSTGRES

<div style="color:orange">
> airflow db init 
</div>


##### CREAR USUARIO

<div style="color:orange">
> airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@admin.org 
</div>

##### COMPROBAR USUARIO

<div style="color:orange">
> airflow users list 
</div>

## 1.2. Webserver

<div style="color:orange">
> airflow webserver --port 8080
</div>


## 1.3. Scheduler

<div style="color:orange">
> airflow scheduler
</div>


# 3. DAGS


## 01-check_file

Comprobar que un fichero existe en la ruta dada. Para ello usamos un **BashOperator** que ejecuta un script de bash.

Con este DAG aprenderemos:
<div style="color:orange">
    
    
- Configurar Dags: parámetro, intervalos, programación...

- Visualización de Dags en la web: Ver programación, estado del DAG, historial, logs...

- Añadir markdown en DAG y las tareas (instance details).

- BashOperator.
    
 </div>


```python
BashOperator(
    task_id='check_file',
    bash_command='sh ' + absolute_bash_file_path  + ' ' + absolute_file_path 
)
```

## 02-load-csv-to-GC

Subir un fichero (en este caso csv) a un bucket de **Google Cloud Storage**.

Con este DAG aprenderemos:

<div style="color:orange">
    
    
- PythonOperator.

- Configuración de variables.

- Organización de tareas de un DAG.

 </div> 


```python
PythonOperator(
    task_id='upload_csv_to_gcs',
    python_callable=upload_csv_to_gcs,
    #op_args=[absolute_file_path, bucket_name, destination_file_path]
    op_kwargs={ 
        'file_path': absolute_file_path,
        'bucket_name': bucket_name,
        'destination_file_path': destination_file_path
     }   
)
```

## 03-load-data-to-big-query

Añadir datos almacenados en **Google Cloud Storage** a **Big Query**.

<div style="color:orange">

- GCSToBigQueryOperator.

- Configuración de conexiones.

 </div> 


```python
GCSToBigQueryOperator(
    task_id='load_data_to_big_query',
    bucket=bucket_name,
    source_objects=[destination_file_path], # Todos los elementos del bucket
    source_format='CSV', # Formato de los archivos a insertar
    skip_leading_rows=1, # No considerar la primera fila como datos porque la primera fila son las cabeceras
    field_delimiter=',', # Delimitador
    destination_project_dataset_table='airflow-388217.external_data.enquestes', # id de la tabla + el nombre
    create_disposition='CREATE_IF_NEEDED', # Crearla si no existe
    write_disposition='WRITE_APPEND', # Añade a los datos existentes
    bigquery_conn_id='google_cloud_default', # Valor por defecto
    google_cloud_storage_conn_id='google_cloud_default' # Valor por defecto
)
```

 
## 04-load-filtered-data-to-big-query

Añadir datos desde una tabla de **Big Query** a otra filtrando a través de una query.

<div style="color:orange">

- BigQueryExecuteQueryOperator.

 </div>  


```python
BigQueryExecuteQueryOperator(
    task_id='create_table_exiample',
    sql=query,
    destination_dataset_table=dataset_table_eixample,
    write_disposition='WRITE_TRUNCATE', # Eliminar los datos antes de volver a escribir
    create_disposition='CREATE_IF_NEEDED',
    use_legacy_sql=False,
    #bigquery_conn_id='google_cloud_default'
)
```

 

## 05-remove-local-file

Borrar csv de origen, un a vez se han ingestado en el bucket.

<div style="color:orange">

- Paralelización de tareas.

 </div> 




   
    
 
 

 
 
 
## 06-email-on-finish

Enviar un correo

<div style="color:orange">

- EmailOperator.

 </div>  


```python
EmailOperator(
        task_id='send_email',
        to=dest_email,
        subject='La ejecución del dag ' + dag_args['dag_id'] +' correcta',
        html_content=f'''<h3>ÉXITO EN LA EJECUCIÓN!!</h3> <p>La ejecución del dag {dag_args['dag_id']} ha acabado correctamente :)</p> ''',
        dag=dag
)
```