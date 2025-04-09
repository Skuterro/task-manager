from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer, RegisterSerializer, MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from .filters import TaskFilter, TaskHistoryFilter

class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [AllowAny]

class TaskGetUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def perform_update(self, serializer):
        task = serializer.save()

        TaskHistory.objects.create(
            task = task,
            name = task.name, 
            description = task.description,
            status = task.status,
            assigned_to = task.assigned_to,
            action_type='updated', 
            changed_by = self.request.user
        )

class TaskCreateAPIView(generics.CreateAPIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.save()

        TaskHistory.objects.create(
            task=task,
            name=task.name,
            description=task.description,
            status=task.status,
            assigned_to=task.assigned_to,
            action_type='created',
            changed_by=self.request.user
        )

class CurrentUserTaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(assigned_to=self.request.user)
    
class UserTaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assigned_to=user_id)

class TaskHistoryListAPIView(generics.ListAPIView):
    queryset = TaskHistory.objects.all().order_by('-changed_at')
    serializer_class = TaskHistorySerializer
    filterset_class = TaskHistoryFilter
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer