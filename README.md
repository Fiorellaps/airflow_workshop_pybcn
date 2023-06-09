[<img align="left" src="https://pybcn.org/images/logo.png" alt="español" width="150"/>](https://pybcn.org/events/pydatabcn/pydatabcn_2023/) 

[<img align="right" src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="inglés" width="47"/>](https://www.linkedin.com/in/fiorella-piriz-sapio-74569a188/)


<br/>
<br/>

# Orquestación de datos en Airflow

## Índice
1. [Prerrequisitos](#Prerrequisitos)
2. [Instalar Apache Airflow](#Instalar-Apache-Airflow)
3. [Configurar Apache Airflow](#Configurar-Apache-Airflow)
4. [Arrancar Airflow](#Arrancar-Airflow)
5. [Crear cuenta gratuita en Google Cloud Platform](#Crear-cuenta-gratuita-en-Google-Cloud-Platform)


## Prerrequisitos

- Subsistema de Linux (Se recomienda instalarlo en una máquina virtual de Linux, en docker o en Kubernetes, más información en la [documentación oficial](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html))

   Si estamos en Windows podemos habilitarlo con los siguientes pasos:

   1. Ejecutar el Powershell como administrados
   2. Ejecutar el siguiente comando para habilitar el subsistema de Linux:

   `.\Dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`

   3. Reiniciar la máquina

   4. Instalar Ubuntu desde Microsoft Store

   5. Abrir la consola de Ubuntu y ejecutar el siguiente comando para actualizar las librerías del sistema
   
      `sudo apt update`

   6. Localiza disco C: o D: en /mnt
   
      `cd /mnt/c/Users/xxx/Downloads`

- Versión de Python>=3

  `python --version`

- pip3 instalado

  `sudo apt install python3-pip`
  
  Comprobar la versión:
  
  `pip3.exe --version`

## Instalar Apache Airflow

Configurar Airflow Home (en caso de que queramos que sea distinta a /root/airflow)

`nano ~/.bashrc`

Añadir la siguiente línea (no se deben añadir espacio antes ni después del =) y cerrar la ventana de la máquina de Linux

`export AIRFLOW_HOME=/{RUTA A LA NUEVA AIRFLOW HOME}`

Al volver abrir el terminal podemos comprobar que la variable se ha configurado correctamente

`echo $AIRFLOW_HOME`

Inatalación usando desde Pypi
Es recomendable crear un entorno de Python con virtualenv o conda

`pip3.exe install "apache-airflow==2.6.1"`

ahora podemos verificar la versión de airflow instalada

`airflow.exe version`

## Configurar Apache Airflow

Abrimos el fichero de configuración de airflow y lo editamos

`cd $AIRFLOW_HOME`

`nano airflow.cfg`

(Opcional) Deshabilitamos la carga de Dags de ejemplo, Modificando la variable **'load_examples = False'**

## Arrancar Airflow

1. Inicializamos la base de datos

`airflow db init`

2. Crear un usuario

`airflow users create \
--username admin \
--firstname admin \
--lastname admin \
--role Admin \
--email admin@admin.org`
(Introducir contraseña en el prompt)

Comprobar usuario con:
`airflow users list`

3. Arrancar el webserver

`airflow webserver --port 8080` (el puerto por defecto es el 8080)

4. Arrancar el scheduler (en otro terminal o con el webserver arrancado en segundo plano)

`airflow scheduler`

## Crear cuenta gratuita en Google Cloud Platform
(https://console.cloud.google.com/welcome?project=thorn-technologies-public)

Pasos opcionales, pues ya se verán en el workshop, pero se recomienda probar la plataforma de GCP si no se ha usado nunca.

- Añadir un proyecto
- Habilitar el servicio de BigQuery
- Habilitar el servicio de Cloud Storage
- Habilitar el servicio de Cloud Dataproc API 
- Crear un bucket en Cloud Storage
