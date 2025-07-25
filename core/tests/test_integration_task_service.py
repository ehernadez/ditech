import unittest
from unittest.mock import MagicMock
from core.services.integration_task_service import IntegrationTaskService
from core.models import User, IntegrationTask
import uuid

class IntegrationTaskServiceTest(unittest.TestCase):
    def setUp(self):
        self.username = f"servicetest_{uuid.uuid4()}"
        self.user = User.objects.create(username=self.username)
        self.mock_repo = MagicMock()
        self.service = IntegrationTaskService(repository=self.mock_repo)
        self.task = IntegrationTask(id=1, user=self.user, task_name='Service Task', config={'base_url': 'http://test.com', 'http_method': 'GET'})

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_create_task(self):
        self.mock_repo.create_task.return_value = self.task
        result = self.service.create_task(self.user, 'Service Task', {'base_url': 'http://test.com', 'http_method': 'GET'})
        self.assertEqual(result, self.task)

    def test_get_tasks_by_user(self):
        self.mock_repo.get_tasks_by_user.return_value = [self.task]
        result = self.service.get_tasks_by_user(self.user)
        self.assertIn(self.task, result)

    def test_get_task_by_id_found(self):
        self.mock_repo.get_task_by_id.return_value = self.task
        result = self.service.get_task_by_id(1, self.user)
        self.assertEqual(result, self.task)

    def test_get_task_by_id_not_found(self):
        self.mock_repo.get_task_by_id.return_value = None
        with self.assertRaises(Exception):
            self.service.get_task_by_id(999, self.user)

    def test_update_task(self):
        self.mock_repo.get_task_by_id.return_value = self.task
        self.mock_repo.update_task.return_value = self.task
        result = self.service.update_task(1, self.user, 'Updated', {'base_url': 'http://new.com', 'http_method': 'POST'})
        self.assertEqual(result, self.task)

    def test_delete_task(self):
        self.mock_repo.get_task_by_id.return_value = self.task
        self.mock_repo.delete_task.return_value = None
        result = self.service.delete_task(1, self.user)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
