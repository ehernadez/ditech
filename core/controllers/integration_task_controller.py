from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.containers import Container
from core.services.integration_task_service import IntegrationTaskService
from core.serializers import IntegrationTaskSerializer

class IntegrationTaskViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, service=None, repository=None, **kwargs):
        super().__init__(**kwargs)
        self.repository = repository or Container.repository()
        self.service = service or IntegrationTaskService(repository=self.repository)

    @action(detail=False, methods=['get'])
    def get_tasks(self, request):
        tasks = self.service.get_tasks_by_user(request.user)
        serializer = IntegrationTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        task_name = request.data.get('name')
        if not task_name:
            return Response({"error": "El campo 'name' es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        config = request.data.get('config')

        if not config:
            return Response({"error": "El campo 'config' es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(config, dict):
            return Response(
                {
                    "error": "La configuración debe ser un objeto JSON válido, los campos con * son obligatorios",
                    "example config": {
                        "base_url *": "https://api.example.com",
                        "http_method *": "GET",
                        "payload": {}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST)
        
        task = self.service.create_task(request.user, task_name, config)
        serializer = IntegrationTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        if not pk:
            return Response({"error": "El ID de la tarea es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        task_name = request.data.get('name')
        if task_name == '':
            return Response({"error": "El campo 'name' no puede estar vacio"}, status=status.HTTP_400_BAD_REQUEST)
        
        config = request.data.get('config', {})
        if not isinstance(config, dict):
            return Response(
                {
                    "error": "La configuración debe ser un objeto JSON válido, los campos con * son obligatorios",
                    "example config": {
                        "base_url *": "https://api.example.com",
                        "http_method *": "GET",
                        "payload": {}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST)

        task = self.service.update_task(pk, request.user, task_name, config)
        serializer = IntegrationTaskSerializer(task)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "El ID de la tarea es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        self.service.delete_task(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='execute/(?P<pk>[^/.]+)')
    def execute(self, request, pk=None):
        if not pk:
            return Response({"error": "El ID de la tarea es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        self.service.execute_task(pk, request.user)
        return Response({"detail": "Tarea enviada para ejecución", "task_id": pk}, status=status.HTTP_202_ACCEPTED)