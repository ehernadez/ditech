from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

class IntegrationTask(models.Model):

    STATUS_TASK_CHOICES = [
        ('pending', 'Pendiente'),
        ('executed', 'Ejecutada'),
    ]

    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_TASK_CHOICES, default='pendiente')
    execution_time = models.DateTimeField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    config = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integration_tasks')

    def __str__(self):
        return f"{self.task_name} - {self.status} por {self.user.username}"
