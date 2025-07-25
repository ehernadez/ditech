# Orquestador - Prueba Técnica

Este proyecto es un orquestador de tareas de integración desarrollado con Django, Celery y Docker. Permite la gestión y ejecución asíncrona de tareas HTTP mediante una API REST.

## Requisitos
- Docker y Docker Compose
- Python 3.9+

## Instalación y Ejecución

### 1. Clona el repositorio
```sh
git clone https://github.com/ehernadez/ditech.git
cd ditech
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

### 6. Acceso y autenticación
Para probar la API necesitas un usuario registrado y un token JWT.

#### Crear un superusuario (admin)
En una terminal ejecuta:
```powershell
docker compose exec web python manage.py createsuperuser
```
Sigue las instrucciones para crear el usuario y contraseña desde la terminal.

#### Obtener un token JWT
Haz un POST a `/api/token/` con el usuario y contraseña creados:
```json
{
  "username": "<tu_usuario>",
  "password": "<tu_contraseña>"
}
```
Puedes usar [Postman](https://www.postman.com/) para probar:
```powershell
http POST http://localhost:8000/api/token/ username=<tu_usuario> password=<tu_contraseña>
```
El token lo usas en el header `Authorization: Bearer <token>` para acceder a los endpoints protegidos.

#### Crear usuario desde Django admin
> **Nota:** También puedes crear usuarios fácilmente desde la interfaz de administración en [http://localhost:8000/admin](http://localhost:8000/admin) usando el superusuario creado. ¡Accede al panel y agrega usuarios desde la web!

### 7. Accede a la API
- La API estará disponible en: [http://localhost:8000](http://localhost:8000)
- Endpoints principales:
  - `/integration-tasks/` (GET, POST, PUT, DELETE)
  - `/integration-tasks/execute/<id>/` (POST) para ejecutar una tarea asíncrona

### 8. Documentación Swagger/OpenAPI
- El proyecto incluye documentación con **drf-spectacular**.
- Accede a la documentación en: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- El esquema OpenAPI lo puedes descargar en: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- Los ejemplos de request y los campos obligatorios están definidos en la documentación y en los serializers.

### 9. Verifica logs de Celery
Para ver el seguimiento de las tareas ejecutadas:
```powershell
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
