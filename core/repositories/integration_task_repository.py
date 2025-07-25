from django.utils import timezone
from core.models import IntegrationTask
from core.interfaces.integration_task_repository_interface import IIntegrationTaskRepository

class IntegrationTaskRepository(IIntegrationTaskRepository):

    def create_task(self, user, task_name, config):
        task = IntegrationTask(
            user=user,
            task_name=task_name,
            config=config
        )
        task.save()
        return task

    def get_tasks_by_user(self, user):
        return IntegrationTask.objects.filter(user=user).order_by('-created_at')
    
    def get_task_by_id(self, task_id, user):
        try:
            return IntegrationTask.objects.get(id=task_id, user=user)
        except IntegrationTask.DoesNotExist:
            return None
        
    def update_task(self, task, task_name=None, config=None):
        if task_name:
            task.task_name = task_name
        if config:
            task.config = config
        task.save()
        return task

    def mark_task_as_executed(self, task, result=None):
        import logging
        logger = logging.getLogger("celery.task")
        logger.info(f"[Celery] Actualizando tarea {task.id} a 'executed' con resultado: {result}")
        print(f"[Celery] Actualizando tarea {task.id} a 'executed' con resultado: {result}")
        # Refresca el objeto desde la base de datos antes de modificarlo
        task.refresh_from_db()
        task.status = 'executed'
        task.execution_time = timezone.now()
        task.result = result
        task.save()
        logger.info(f"[Celery] Tarea {task.id} actualizada correctamente.")
        print(f"[Celery] Tarea {task.id} actualizada correctamente.")
        return task

    def delete_task(self, task):
        task.delete()