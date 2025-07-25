import unittest
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.controllers.integration_task_controller import IntegrationTaskViewSet
from core.models import User
from unittest.mock import MagicMock
from rest_framework import status
import uuid

class IntegrationTaskControllerTest(unittest.TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # Usa un nombre de usuario único por test
        self.username = f"controlleruser_{uuid.uuid4()}"
        self.user = User.objects.create(username=self.username)
        self.mock_service = MagicMock()
        self.viewset = IntegrationTaskViewSet(service=self.mock_service)

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def drf_request(self, request):
        request.user = self.user
        return Request(request)

    def test_get_tasks_empty(self):
        request = self.factory.get('/integration-tasks/')
        drf_request = self.drf_request(request)
        self.mock_service.get_tasks_by_user.return_value = []
        response = self.viewset.get_tasks(drf_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_tasks_with_data(self):
        self.mock_service.get_tasks_by_user.return_value = [MagicMock()]
        request = self.factory.get('/integration-tasks/')
        drf_request = self.drf_request(request)
        response = self.viewset.get_tasks(drf_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_missing_pk(self):
        request = self.factory.put('/integration-tasks/', {'name': 'Updated', 'config': {'base_url': 'http://new.com', 'http_method': 'POST'}}, format='json', HTTP_CONTENT_TYPE='application/json')
        drf_request = self.drf_request(request)
        response = self.viewset.update(drf_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_missing_pk(self):
        request = self.factory.delete('/integration-tasks/')
        drf_request = self.drf_request(request)
        response = self.viewset.delete(drf_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        request = self.factory.delete('/integration-tasks/1/')
        drf_request = self.drf_request(request)
        self.mock_service.delete_task.return_value = None
        response = self.viewset.delete(drf_request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_execute_missing_pk(self):
        request = self.factory.post('/integration-tasks/execute/')
        drf_request = self.drf_request(request)
        response = self.viewset.execute(drf_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_execute_success(self):
        request = self.factory.post('/integration-tasks/execute/1/')
        drf_request = self.drf_request(request)
        self.mock_service.execute_task.return_value = None
        response = self.viewset.execute(drf_request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

if __name__ == "__main__":
    unittest.main()
