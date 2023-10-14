# proyecto-202314  

## Tabla de contenido

- [Pre-requisitos para el microservicio route](#pre-requisitos)
- [Estructura de cada microservicio](#estructura-de-cada-microservicio)
  - [Archivos de soporte](#archivos-de-soporte)
  - [Carpeta src](#carpeta-src)
  - [Carpeta test](#carpeta-test)
- [Ejecutar un microservicio](#ejecutar-un-microservicio)
  - [Instalar dependencias](#instalar-dependencias)
  - [Variables de entorno](#variables-de-entorno)
  - [Ejecutar el servidor](#ejecutar-el-servidor)
  - [Ejecutar pruebas](#ejecutar-pruebas)
  - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
- [Ejecutar Docker Compose](#ejecutar-docker-compose)
- [Ejecutar Colección de Postman](#ejecutar-colección-de-postman)
- [Ejecutar evaluador github action workflow](#ejecutar-evaluador-github-action-workflow)

## Pre-requisitos
- Python ~3.10
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

## Estructura de cada microservicio
Cada microservicio utiliza Python y Flask para ejecutar el servidor, y unittest para ejecutar las pruebas unitarias. En general, dentro de cada uno de ellos hay dos carpetas principales: `src` y `tests`.

### Archivos de soporte
- `requirements.txt`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. Consulta la sección **Instalar dependencias**.
- `.env`: Archivo Env utilizado para definir variables de entorno. 

### Carpeta src
Esta carpeta contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio, así como para la comunicación con la base de datos. Hay 4 carpetas principales:
- `/models`: Esta carpeta contiene la capa de persistencia, donde se declaran los modelos que se van a persistir en la base de datos en forma de tablas, así como la definición de cada columna. Incluimos un archivo `route.py` que contiene un modelo base llamado `Route`, que realiza la configuración básica de una tabla. Por ejemplo:
```python
# /models/car.py
from ..database import database
from sqlalchemy import Column, String, DateTime, Float


class Route(database.Base):

    __tablename__ = 'route'

    id = Column(String, primary_key=True)
    flightId = Column(String)
    sourceAirportCode = Column(String)
    sourceCountry = Column(String)
    destinyAirportCode = Column(String)
    destinyCountry = Column(String)
    bagCost = Column(Float)
    plannedStartDate = Column(DateTime)
    plannedEndDate = Column(DateTime)
    createdAt = Column(DateTime)
    updateAt = Column(DateTime)
```
 - *controllers* Esta carpeta contiene la capa de aplicación de nuestro microservicio, responsable de declarar cada servicio API que estamos exponiendo. `ping.py` `route.py` `reset.py`
 - *./database* crea la base de datos durante el deployment de la api
 - *./services* modela la lógica de negocio del API `route.py`

### Carpeta test
Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`

## Ejecutar un microservicio
### Instalar dependencias
Utilizamos pip para gestionar las dependencias, inicia el shell de venv para activar el entorno virtual con el siguiente comando:

```bash
$> python -m venv venv
$> source /venv/bin/activate
``` 
Luego ejecuta el comando de instalación.
```bash
$> pip install -r requirements.txt
```
Esto instalará las dependencias solo dentro del entorno virtual, así que recuerda activarlo cuando estés trabajando con el microservicio.

Para salir del entorno virtual, utiliza el siguiente comando:
```bash
$> deactivate
```

### Variables de entorno

El servidor Flask y las pruebas unitarias utilizan variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución. A alto nivel, esas variables son:
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres
- USERS_PATH: Para los microservicios que se comunican con el microservicio de Usuarios, necesitas especificar esta variable de entorno que contiene la URL utilizada para acceder a los endpoints de usuarios. (Ejemplo: http://localhost:3000, http://users-service)

Estas variables de entorno deben especificarse en `.env` en la raíz de la carpeta del microservicio.


### Ejecutar el servidor
Una vez que las variables de entorno estén configuradas correctamente, para ejecutar el servidor utiliza el siguiente comando:
```bash

$> gunicorn -b 0.0.0.0:<PORT_TO_RUN_SERVER> app:app

# Routes
$> gunicorn -b 0.0.0.0:3002 app:app


```
### Ejecutar pruebas
Para ejecutar las pruebas unitarias de los microservicios y establecer el porcentaje mínimo de cobertura del conjunto de pruebas en 70%, ejecuta el siguiente comando:
```bash
python -m unittest discover tests
coverage run --source=src -m unittest discover tests
          coverage report -m
          coverage_percentage=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if [ "$coverage_percentage" -lt 70 ]; then
            echo "Coverage is below 70% (current: $coverage_percentage%). Exiting with error."
            exit 1
          else
            echo "Coverage is acceptable ($coverage_percentage%)."
          fi
```
### Ejecutar desde Dockerfile
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:
```bash
$> docker build -t route-management:v0.0.1 .
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run route-management:v0.0.1
```

## Ejecutar Docker Compose
Para ejecutar el microservicio de route al mismo tiempo con la base de datos. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash


$> docker-compose -f "docker-compose.yml" up --build
```

## Ejecutar Colección de Postman
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/monitor-202314/main/entrega1/entrega1.json


Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

## Ejecutar evaluador github action workflow

Para ejecutar el workflow, ve a la sección de "Actions" del repositorio que se encuentra en la parte superior.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/92d686b7-21b1-42b1-b23a-e8c3d626dfd3" alt="Screenshot" width="800">

Luego, encontrarás en la sección izquierda una lista de todos los flujos de trabajo (workflows) disponibles para ejecución. En este caso, verás "Evaluator_Entrega1". Haz clic en el que deseas ejecutar. Verás un botón "Run workflow" en la sección superior derecha, haz clic en este botón, selecciona la rama en la que deseas ejecutarlo y haz clic en el botón "Run workflow".

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/4bcf1c0d-e422-4f9d-9ff6-a663f8248352" alt="Screenshot" width="800">

Esto iniciará la ejecución del workflow en la rama. Si todo funciona correctamente y la entrega es correcta, verás que todas las comprobaciones aparecen como aprobadas (passed).

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/c6c580b2-80e0-411d-8971-a252312ce5ea" alt="Screenshot" width="800">
