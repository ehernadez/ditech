from orquestador.celery import app
from core.containers import Container
from django.contrib.auth import get_user_model
import requests
import time
import logging

@app.task
def execute_integration_task_async(task_id, user_id):
    logger = logging.getLogger("celery.task")
    logger.info(f"[Celery] Iniciando ejecución de tarea {task_id} para usuario {user_id}")
    User = get_user_model()
    repository = Container.repository()
    result = None
    try:
        user = User.objects.get(id=user_id)
        task = repository.get_task_by_id(task_id, user)
        if not task:
            logger.warning(f"[Celery] Tarea {task_id} no encontrada para usuario {user_id}")
            return
        # Espera al menos dos segundos antes de continuar
        time.sleep(2)
        base_url = task.config.get('base_url')
        http_method = task.config.get('http_method').upper()
        payload = task.config.get('payload', {})
        logger.info(f"[Celery] Ejecutando petición {http_method} a {base_url} con payload: {payload}")
        try:
            if http_method == 'GET':
                response = requests.get(base_url, timeout=5)
            elif http_method == 'POST':
                response = requests.post(base_url, json=payload, timeout=5)
            elif http_method == 'PUT':
                response = requests.put(base_url, json=payload, timeout=5)
            elif http_method == 'DELETE':
                response = requests.delete(base_url, timeout=5)
            result = response.json() if response.status_code == 200 else None
        except Exception as e:
            result = {'error': str(e)}
            logger.error(f"[Celery] Error en la petición: {e}")
        repository.mark_task_as_executed(task, result)
    except Exception as e:
        logger.error(f"[Celery] Error general en la tarea: {e}")
