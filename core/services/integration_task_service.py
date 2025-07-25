import time
import requests
from rest_framework import exceptions
from core.interfaces.integration_task_repository_interface import IIntegrationTaskRepository
from core.interfaces.integration_task_service_interface import IIntegrationTaskService
from core.jobs.integration_task_job import execute_integration_task_async

class IntegrationTaskService(IIntegrationTaskService):
    def __init__(self, repository: IIntegrationTaskRepository):
        self.repository = repository

    def create_task(self, user, task_name, config):
        return self.repository.create_task(user, task_name, config)

    def get_tasks_by_user(self, user):
        return self.repository.get_tasks_by_user(user)

    def get_task_by_id(self, task_id, user):
        task = self.repository.get_task_by_id(task_id, user)
        if not task:
            raise exceptions.NotFound("Tarea no encontrada")
        return task

    def update_task(self, task_id, user, task_name=None, config=None):
        task = self.repository.get_task_by_id(task_id, user)
        if not task:
            raise exceptions.NotFound("Tarea no encontrada")
        return self.repository.update_task(task, task_name, config)

    def execute_task(self, task_id, user):
        execute_integration_task_async.delay(task_id, user.id)

    def delete_task(self, task_id, user):
        task = self.repository.get_task_by_id(task_id, user)
        if not task:
            raise exceptions.NotFound("Tarea no encontrada")
        return self.repository.delete_task(task)