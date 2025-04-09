import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from task_manager_app.models import Task, TaskHistory

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="test123",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )

@pytest.fixture
def task(db, user):
    """Tworzy zadanie przypisane do użytkownika."""
    return Task.objects.create(
        name="Test Task",
        description="Test Description",
        status="new",
        assigned_to=user
    )

# Testy endpointów

@pytest.mark.django_db
def test_task_create(client, user):
    """Testuje POST /tasks/create/"""
    client.force_authenticate(user=user)
    data = {
        "name": "New Task",
        "description": "New Description",
        "status": "new",
        "assigned_to": user.id
    }
    response = client.post("/tasks/create/", data, format="json")
    assert response.status_code == 201
    assert Task.objects.count() == 1
    assert TaskHistory.objects.count() == 1 
    assert response.data["name"] == "New Task"

@pytest.mark.django_db
def test_task_create_no_desc(client, user):
    """Testuje POST /tasks/create/"""
    client.force_authenticate(user=user)
    data = {
        "name": "New Task without desc",
        "description": "",
        "status": "new",
        "assigned_to": user.id
    }
    response = client.post("/tasks/create/", data, format="json")
    assert response.status_code == 201
    assert Task.objects.count() == 1
    assert TaskHistory.objects.count() == 1 
    assert response.data["name"] == "New Task without desc"

@pytest.mark.django_db
def test_task_list(client, task):
    """Testuje GET /tasks/ """
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Task"
    assert response.data[0]["status"] == "new"

@pytest.mark.django_db
def test_task_detail(client, task):
    """Testuje GET /tasks/<task_id>/ """
    response = client.get(f"/tasks/{task.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "Test Task"
    assert response.data["description"] == "Test Description"

@pytest.mark.django_db
def test_task_update(client, user, task):
    """Testuje PUT /tasks/<task_id>/ """
    client.force_authenticate(user=user)
    data = {
        "name": "Updated Task",
        "description": "Updated Description",
        "status": "in_progress",
        "assigned_to": user.id
    }
    response = client.put(f"/tasks/{task.id}/", data, format="json")
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.name == "Updated Task"
    assert task.status == "in_progress"
    assert TaskHistory.objects.count() == 1

@pytest.mark.django_db
def test_task_patch(client, user, task):
    """Testuje PATCH /tasks/<task_id>/ """
    client.force_authenticate(user=user)
    data = {
        "status": "in_progress"
    }
    response = client.patch(f"/tasks/{task.id}/", data, format="json")
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.name == "Test Task" 
    assert task.description == "Test Description" 
    assert task.status == "in_progress" 
    assert TaskHistory.objects.count() == 1 

@pytest.mark.django_db
def test_task_delete(client, admin_user, task):
    """Testuje DELETE /tasks/<task_id>/ """
    client.force_authenticate(user=admin_user) 
    response = client.delete(f"/tasks/{task.id}/")
    assert response.status_code == 204
    assert Task.objects.count() == 0

@pytest.mark.django_db
def test_current_user_tasks(client, user, task):
    """Testuje GET /user-tasks/ """
    client.force_authenticate(user=user)
    response = client.get("/user-tasks/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Task"

@pytest.mark.django_db
def test_user_tasks(client, admin_user, user, task):
    """Testuje GET /tasks/user/<user_id>/"""
    client.force_authenticate(user=admin_user)
    response = client.get(f"/tasks/user/{user.id}/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Task"

@pytest.mark.django_db
def test_task_history(client, user, task):
    """Testuje GET /history/ """
    TaskHistory.objects.create(
        task=task,
        name=task.name,
        description=task.description,
        status=task.status,
        assigned_to=task.assigned_to,
        action_type="created",
        changed_by=user
    )
    client.force_authenticate(user=user)
    response = client.get("/history/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["action_type"] == "created"

@pytest.mark.django_db
def test_register(client):
    """Testuje POST /register/"""
    data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "test123!",
        "password2": "test123!",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post("/register/", data, format="json")
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get(username="newuser").check_password("test123!")

@pytest.mark.django_db
def test_login(client, user):
    """Testuje POST /login/"""
    data = {
        "username": "testuser",
        "password": "test123"
    }
    response = client.post("/login/", data, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data