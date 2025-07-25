from abc import ABC, abstractmethod

class IIntegrationTaskRepository(ABC):
    @abstractmethod
    def create_task(self, user, task_name, config):
        pass

    @abstractmethod
    def get_tasks_by_user(self, user):
        pass

    @abstractmethod
    def get_task_by_id(self, task_id, user):
        pass

    @abstractmethod
    def update_task(self, task, task_name=None, config=None):
        pass

    @abstractmethod
    def mark_task_as_executed(self, task, result=None):
        pass

    @abstractmethod
    def delete_task(self, task):
        pass
