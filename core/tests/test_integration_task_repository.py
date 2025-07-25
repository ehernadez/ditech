import unittest
from core.models import IntegrationTask, User
from core.repositories.integration_task_repository import IntegrationTaskRepository
from django.utils import timezone
import uuid

class IntegrationTaskRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.username = f"testuser_{uuid.uuid4()}"
        self.user = User.objects.create(username=self.username)
        self.repo = IntegrationTaskRepository()
        self.task = self.repo.create_task(self.user, 'Test Task', {'base_url': 'http://test.com', 'http_method': 'GET'})

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_create_task(self):
        self.assertIsInstance(self.task, IntegrationTask)
        self.assertEqual(self.task.task_name, 'Test Task')

    def test_get_tasks_by_user(self):
        tasks = self.repo.get_tasks_by_user(self.user)
        self.assertIn(self.task, tasks)

    def test_get_task_by_id(self):
        found = self.repo.get_task_by_id(self.task.id, self.user)
        self.assertEqual(found, self.task)

    def test_update_task(self):
        updated = self.repo.update_task(self.task, task_name='Updated', config={'base_url': 'http://new.com', 'http_method': 'POST'})
        self.assertEqual(updated.task_name, 'Updated')
        self.assertEqual(updated.config['base_url'], 'http://new.com')

    def test_mark_task_as_executed(self):
        result = {'data': 'ok'}
        executed = self.repo.mark_task_as_executed(self.task, result)
        self.assertEqual(executed.status, 'executed')
        self.assertEqual(executed.result, result)
        self.assertIsNotNone(executed.execution_time)

    def test_delete_task(self):
        self.repo.delete_task(self.task)
        self.assertIsNone(self.repo.get_task_by_id(self.task.id, self.user))

if __name__ == "__main__":
    unittest.main()
