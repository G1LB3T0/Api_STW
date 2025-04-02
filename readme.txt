# API de Gestión de Incidentes

Esta es una API REST desarrollada con Flask para la gestión de incidentes. Permite crear, leer, actualizar y eliminar incidentes con sus respectivos estados.

## Requisitos Previos

- Python 3.x
- PostgreSQL
- pip (gestor de paquetes de Python)

## Configuración de la Base de Datos

1. Instalar PostgreSQL en tu sistema
2. Crear una base de datos llamada 'api'
3. Configurar PostgreSQL con los siguientes parámetros:
   - Usuario: postgres
   - Contraseña: paris12ysolo12
   - Puerto: 5432
   - Host: localhost

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias:
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-marshmallow
pip install marshmallow-sqlalchemy
pip install psycopg2
```

## Ejecución

Para iniciar el servidor:
```bash
python app.py
```

El servidor se ejecutará en `http://localhost:3001`

## Endpoints Disponibles

### GET /
- Ruta raíz que muestra un mensaje de bienvenida

### POST /incidents
- Crear un nuevo incidente
- Requiere:
  - reporter (string): Nombre del reportante
  - description (string): Descripción del incidente (mínimo 10 caracteres)

### GET /incidents
- Obtener todos los incidentes

### GET /incidents/<id>
- Obtener un incidente específico por ID

### PUT /incidents/<id>
- Actualizar el estado de un incidente
- Estados permitidos: 'pendiente', 'en proceso', 'resuelto'

### DELETE /incidents/<id>
- Eliminar un incidente por ID

## Estructura de Datos

### Incidente
- id: Identificador único (autoincremental)
- reporter: Nombre del reportante
- description: Descripción del incidente
- status: Estado del incidente (pendiente/en proceso/resuelto)
- created_at: Fecha y hora de creación

## Ejemplos de Uso

### Crear un Incidente
```bash
curl -X POST http://localhost:3001/incidents \
-H "Content-Type: application/json" \
-d '{"reporter": "Juan Pérez", "description": "Error en el sistema de login"}'
```

### Obtener Todos los Incidentes
```bash
curl http://localhost:3001/incidents
```

### Actualizar Estado de un Incidente
```bash
curl -X PUT http://localhost:3001/incidents/1 \
-H "Content-Type: application/json" \
-d '{"status": "en proceso"}'
```

### Eliminar un Incidente
```bash
curl -X DELETE http://localhost:3001/incidents/1
``` 