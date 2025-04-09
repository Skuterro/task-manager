from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(), name='tasks'),
    path('user-tasks/', views.CurrentUserTaskListAPIView.as_view(), name='logged-user-tasks'),
    path('tasks/<int:task_id>/', views.TaskGetUpdateDeleteAPIView.as_view(), name='get-update-delete-task'),
    path('tasks/create/', views.TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/user/<int:user_id>/', views.UserTaskListAPIView.as_view(), name='user-tasks'),
    path('history/', views.TaskHistoryListAPIView.as_view(), name='tasks-history'),
    path('login/', views.MyObtainTokenPairView.as_view(), name='login-user'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
]