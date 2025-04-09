from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = {
        "new": "Nowy",
        "in_progress": "W toku",
        "resolved": "Rozwiązany",
    }

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
class TaskHistory(models.Model):
    ACTION_CHOICES = (
        ('created', 'Utworzono'),
        ('updated', 'Edytowano'),
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=11)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=7, choices=ACTION_CHOICES, default='created')
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='changed_task_history')
