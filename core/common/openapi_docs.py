from drf_spectacular.utils import extend_schema, OpenApiExample
from core.serializers import IntegrationTaskSerializer

create_task_schema = extend_schema(
    description="Crea una nueva tarea de integración HTTP.",
    request=IntegrationTaskSerializer,
    responses=IntegrationTaskSerializer,
    examples=[
        OpenApiExample(
            'Ejemplo de creación',
            value={
                "name": "Mi tarea",
                "config": {
                    "base_url": "https://api.ejemplo.com",
                    "http_method": "POST",
                    "payload": {"key": "valor"}
                }
            },
            request_only=True
        )
    ]
)

update_task_schema = extend_schema(
    description="Actualiza una tarea de integración existente.",
    request=IntegrationTaskSerializer,
    responses=IntegrationTaskSerializer,
    examples=[
        OpenApiExample(
            'Ejemplo de actualización',
            value={
                "name": "Tarea actualizada",
                "config": {
                    "base_url": "https://api.nuevo.com",
                    "http_method": "PUT",
                    "payload": {"nuevo": "valor"}
                }
            },
            request_only=True
        )
    ]
)

execute_task_schema = extend_schema(
    description="Ejecuta una tarea de integración de forma asíncrona.",
    request=None,
    responses={202: OpenApiExample(
        'Respuesta de ejecución',
        value={"detail": "Tarea enviada para ejecución", "task_id": 1},
        response_only=True
    )}
)

delete_task_schema = extend_schema(
    description="Elimina una tarea de integración.",
    request=None,
    responses={204: None}
)

get_tasks_schema = extend_schema(
    description="Obtiene todas las tareas de integración del usuario autenticado.",
    responses=IntegrationTaskSerializer(many=True)
)
