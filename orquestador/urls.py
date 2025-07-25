from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.controllers.integration_task_controller import IntegrationTaskViewSet
from core.controllers.user_controller import MeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

router = DefaultRouter()
router.register(r'integration-tasks', IntegrationTaskViewSet, basename='integration-tasks')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/user/me/', MeView.as_view(), name='user_me'),
    path('', include(router.urls)),
]