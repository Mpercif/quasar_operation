
[![Python](https://img.shields.io/badge/Python-%32.7-green.svg)](https://www.python.org/downloads/)
[![Python](https://img.shields.io/badge/Python-flask-blue.svg)](https://flask.palletsprojects.com/en/3.0.x/)


# Quasar Operation
### Ejercicio:
El servicio de inteligencia rebelde ha detectado un llamado de auxilio de una nave portacarga imperial a la deriva en un campo de asteroides. El manifiesto de la nave es ultra clasificado, pero se rumorea que transporta raciones y armamento para una legión entera.

- Como jefe de comunicaciones rebelde, tu misión es crear un programa en Golang que retorne la fuente y contenido del mensaje de auxilio. Para esto, cuentas con tres satélites que te permitirán triangular la posición, ¡pero cuidado! el mensaje puede no llegar completo a cada satélite debido al campo de asteroides frente a la nave.

### Consideraciones
- La unidad de distancia en los parámetros de GetLocation es la misma que la que se
utiliza para indicar la posición de cada satélite.
- El mensaje recibido en cada satélite se recibe en forma de arreglo de strings. ● Cuando una palabra del mensaje no pueda ser determinada, se reemplaza por un string en blanco en el array.
  - Ejemplo: [“este”, “es”, “”, “mensaje”]
- Considerar que existe un desfasaje (a determinar) en el mensaje que se recibe en cada
satélite.
  - Kenobi: [“”, “este”, “es”, “un”, “mensaje”]
  - Skywalker: [“este”, “”, “un”, “mensaje”] 
  - Sato: [“”, ””, ”es”, ””, ”mensaje”]

### Mis consideraciones
- La distancia de los satélites debe ser mucho mayor que la de los ejemplos propuestos, ya que las soluciones no convergen.
- El desfase de los mensajes solo se ve afectado al inicio de cada mensaje.


# Quasarservice
## Pre requisitos
* Python 2.7

## Instalar paquetes y bibliotecas.
Crear un ambiente virtual (Opcional)

```bash
virtualenv -p python2 env
```

Activar el ambiente virtual
```bash
source env/bin/activate
```

Instalar librerías y dependencias de Python

```bash
pip install -r requirements.txt  # Development dependencies
```

## DB - Postgres
Debe descargar y crear una instancia de PostgreSQL
```bash
postgresql://postgres:testenv@localhost/mercadolibre
```

Agregar el codigo 
```bash
db.create_all()
```
Al final del archivo `models.py` 

## Ejecutar servicio

```bash
python run.py runserver
```

## Coleccion Api Postman
Puedes usar la colección de Postman para probar el servicio en la nube
```bash
/static/REST_API_ QUASAR_SERVICE.postman_collection
```

## Evidencias de funcionamiento
### POST topsecret
![POST_topsecret](./static/topsecret_POST.png)

### POST topsecret_split
![POST_topsecret_split](./static/topsecret_split_POST.png)

### GET topsecret_split
![GET_topsecret_split](./static/topsecret_split_GET.png)

## Coverage Unit test
![coverage_unit_test](./static/coverage_unit_test.png)

## Api Docs
Puedes ver la información del servicio en 
```bash
http://34.125.136.168/apidocs/
```
![api_docs](./static/api_docs.png)

## Arquitectura 
![arquitectura](./static/Arquitectura.png)










