from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

User = get_user_model()

class UserService:
    def __init__(self):
        self.user_model = User
    
    def get_user_details(self, user_id):
        try:
            user = self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            raise NotFound("Usuario no encontrado")
        return {
            "id": user.id,
            "username": user.username,  
            "email": user.email,
        }