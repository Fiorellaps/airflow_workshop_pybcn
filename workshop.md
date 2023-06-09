# Instalación de Airflow en Linux

Creamos un entorno de Python con virtualenv y lo activamos

`python -m venv env_airflow`


`source airflow_env/bin/ativate`

Definimos AIRFLOW_HOME


`export AIRFLOW_HOME=/mnt/hostapath/airflow`

Instalamos airflow desde Pypi


`pip install "apache-airflow[gcp]"`

Muchos más [providers](https://airflow.apache.org/docs/#providers-packagesdocsapache-airflow-providersindexhtml)

Modificar la configuración de airflow


`nano /root/airflow/airflow.cfg`

- load_examples=False
- sql_alchemy_conn = postgresql+psycopg2://user:pass@localhost:5432/airflow_db

Comprobamos que está bien instalado


`airflow version`

Arrancamos airflow manualmente
\*\* También se podría arrancar usando el comando `airflow standalone` o en modo cluster

1. Inicializamos la base de datos

\*\* PREPARAR EL POSTGRES
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'XXX';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
ALTER ROLE airflow_user SET search_path = public;
https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html

`airflow db init`

2. Crear un usuario

`airflow users create \
--username admin \
--firstname admin \
--lastname admin \
--role Admin \
--email admin@admin.org`

Comprobar usuarios

`airflow users list`

3. Arrcancar el webserver

`airflow webserver -p 8080`
Accedemos a la web en [http://localhost:8080](http://10.251.188.28:8080/)

4. Arrancar el schedule
   `airflow scheduler`

## 01-check_file_dag.py

Comprobar que un fichero existe en la ruta dada. Para elo usamos el BashOperator que ejecuta un script de bash.

Con este dag aprenderemos:

- Configurar Dags: parámetro, intervalos, programación

- Visualización de Dags en la web: Ver programación, estado del Dag, historial, logs

- Añadir markdown en Dag y a las tareas (instance details)

- Creación de variables (base_dag_path). Deficinioneas globales que se omparten en distintos dags

Las variables en Airflow son utilizadas para almacenar y gestionar información que puede ser compartida y utilizada por tareas y DAGs en diferentes contextos. Sirven como un mecanismo para almacenar configuraciones, credenciales, rutas de archivos, parámetros y cualquier otro dato que pueda ser utilizado en el flujo de trabajo de Airflow.

Aquí tienes algunos casos de uso comunes para las variables de Airflow:

Configuración global: Las variables se pueden utilizar para almacenar configuraciones globales que son utilizadas por múltiples DAGs. Por ejemplo, puedes definir una variable llamada s3_bucket para especificar el nombre del bucket de Amazon S3 que se utiliza en varios DAGs.

Credenciales: Las variables son útiles para almacenar credenciales como claves de API, contraseñas o tokens de acceso. Puedes crear una variable llamada aws_credentials y asignarle el valor de las credenciales de AWS, y luego acceder a esa variable desde tus DAGs para autenticar tus operaciones con servicios de AWS.

Parámetros dinámicos: Puedes utilizar variables para definir parámetros dinámicos en tus DAGs. Por ejemplo, puedes crear una variable llamada execution_date_offset que almacene un número que determina el desplazamiento de la fecha de ejecución en tus DAGs.

Rutas de archivos: Las variables pueden contener rutas de archivos o directorios que se utilizan en tus tareas. Esto permite una mayor flexibilidad al especificar rutas y facilita la reutilización de DAGs en diferentes entornos. Por ejemplo, puedes tener una variable llamada data_directory que almacene la ruta al directorio donde se encuentran los datos de entrada para tus tareas.

Las variables de Airflow se pueden administrar a través de la interfaz de usuario de Airflow o utilizando la línea de comandos mediante el comando airflow variables. Puedes definir nuevas variables, modificar o eliminar variables existentes según sea necesario.

En resumen, las variables en Airflow son una forma conveniente de almacenar y compartir información reutilizable en el entorno de tus DAGs, lo que permite una mayor flexibilidad y personalización en tu flujo de trabajo.

## 02-move_csv_to_cloud_storage

1. Primero debemos tener una cuenta configurada en **Google Cloud Console**.

2. Crear un bucket en **Cloud Storage** (ubicación region us-east1)

3. Crear cuenta de servicio en **IAM y Administración**. El usuario tendrá el Rol de Editor.

4. Crear las claves de acceso al usuario creado.

5. Crear función de Python que escriba el csv en Cloud Storage usando el **Python Operator**.

## 03-move_from_cloud_storage_to_big_query

Mirar Operador de Google en la documenación de airflow.

https://airflow.apache.org/docs/

https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/index.html

En concetro nos centramosen el

## 04

5. Crear la conexión a Google Cloud (google_cloud_default). Modificamos el key file path y el nombre del proyecto

## 05

## 06

## Siguientes Pasos

- Airflow code editor

- Xcoms y Xpull
- Templating con macros de airflow
- Operadores de Kubernetes, Spark, Email, etc.
- Datasets
- Taks Groups
- Subdags
- Triggers
- Sincronización de Dags con Git
