from dependency_injector import containers, providers
from core.repositories.integration_task_repository import IntegrationTaskRepository

class Container(containers.DeclarativeContainer):
    repository = providers.Singleton(IntegrationTaskRepository)
