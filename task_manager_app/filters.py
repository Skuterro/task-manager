import django_filters
from .models import Task, TaskHistory

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'id': ['exact'],
            'name': ['icontains'],         
            'description': ['icontains'], 
            'status': ['exact'],     
            'assigned_to': ['exact'],
        }

class TaskHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = TaskHistory
        fields = {
            'task': ['exact'],
            'name': ['icontains'],
            'assigned_to': ['exact'],
            'changed_by':['exact'],
            'changed_at': ['gte', 'lte'],
        }