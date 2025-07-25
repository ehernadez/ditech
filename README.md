# Orquestador - Prueba Técnica

Este proyecto es un orquestador de tareas de integración desarrollado con Django, Celery y Docker. Permite la gestión y ejecución asíncrona de tareas HTTP mediante una API REST.

## Requisitos
- Docker y Docker Compose
- Python 3.9+

## Instalación y Ejecución

### 1. Clona el repositorio
```sh
git clone https://github.com/ehernadez/ditech.git
cd orquestador
```

### 2. Configura las variables de entorno (opcional)
El proyecto ya incluye valores por defecto en `settings.py` para base de datos y Redis.

### 3. Construye y levanta los servicios
```sh
docker compose up --build
```
Esto levantará:
- PostgreSQL (db)
- Redis (redis)
- Django API (web)
- Worker Celery (celery)

### 4. Aplica migraciones
En otra terminal, ejecuta:
```sh
docker compose exec web python manage.py migrate
```

### 5. Ejecuta los tests
Para verificar que todo funciona correctamente:
```sh
docker compose exec web python manage.py test core.tests --verbosity=2
```
Todos los tests deben pasar. Si algún test falla, revisa la sección de troubleshooting.

### 6. Accede a la API
- La API estará disponible en: [http://localhost:8000](http://localhost:8000)
- Endpoints principales:
  - `/integration-tasks/` (GET, POST, PUT, DELETE)
  - `/integration-tasks/execute/<id>/` (POST) para ejecutar una tarea asíncrona

### 7. Documentación Swagger/OpenAPI
- El proyecto incluye documentación con **drf-spectacular**.
- Accede a la documentación en: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- El esquema OpenAPI lo puedes descargar en: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- Los ejemplos de request y los campos obligatorios están definidos en la documentación y en los serializers.

### 8. Verifica logs de Celery
Para ver el seguimiento de las tareas ejecutadas:
```sh
docker compose logs celery
```

## Notas
- Las tareas ejecutadas por Celery actualizan el estado, fecha de ejecucion y resultado en la base de datos.
- Puedes consultar el estado de una tarea con un GET a `/integration-tasks/`.
- El proyecto incluye inyección de dependencias y arquitectura desacoplada para facilitar pruebas y mantenimiento.
- Los tests unitarios están en `core/tests/` y cubren los módulos principales.
- La documentación Swagger/OpenAPI se genera automáticamente y se mantiene centralizada en `core/common/openapi_docs.py`.

## Troubleshooting
- Si algún servicio no levanta, revisa los logs con:
  ```sh
  docker compose logs web
  docker compose logs celery
  ```

## Dependencias principales
- Django
- djangorestframework
- celery
- redis
- requests
- dependency-injector
- djangorestframework-simplejwt
- psycopg2-binary
- drf-spectacular

## Estructura principal
- `core/` - Lógica de negocio, modelos, servicios, repositorios, jobs Celery
- `orquestador/` - Configuración Django y Celery
- `docker-compose.yml` y `Dockerfile` - Contenedores y servicios

---

¿Dudas o problemas? Revisa los logs y asegúrate de que todos los servicios estén levantados correctamente.
