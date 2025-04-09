# Spis treści
- [Uruchomienie](#uruchomienie)
- [Rejestracja nowego użytkownika](#rejestracja-nowego-użytkownika)
- [Autoryzacja](#autoryzacja)
- [Zarządzanie zadaniami](#zarządzanie-zadaniami)
- [Historia zadań](#historia-zadań)
- [Filtrowanie historii i zadań](#filtrowanie-historii-i-zadań)

## Uruchomienie
#### 1.Budowanie projektu
```sh
należy utworzyć plik .env w głownym katalogu z SECRET_KEY
```
```sh
docker compose -f docker-compose.yml up --build
```
### 1.1 Jeżeli projekt budowany jest pierwszy raz, po uruchomieniu bazy danych należy wywołać
```sh
docker exec -it backend python manage.py makemigrations                                    
docker exec -it backend python manage.py migrate
```
Dostęp do aplikacji
```
http://localhost:8000/tasks/
```
### 1.2 Tworzymy admina (przyda się do testowania niektórych endpointów)
```sh
docker-compose exec backend python manage.py createsuperuser
```
## Rejestracja nowego użytkownika
```sh
curl -X POST "http://localhost:8000/register/" \
    -H "Content-Type: application/json" \
    -d '{"username": "newuser", "email": "new@example.com", "password": "test123!", "password2": "test123!", "first_name": "New", "last_name": "User"}'
```
**Odpowiedź:**
```json
{
    "username": "newuser",
    "email": "new@example.com",
    "first_name": "New",
    "last_name": "User"
}
```
## Autoryzacja

```sh
curl -X POST "http://localhost:8000/login/" \
    -H "Content-Type: application/json" \
    -d '{"username": "newuser", "password": "test123!"}'
```
**Odpowiedź:**
```json
{
    "refresh": "TOKEN_REFRESH",
    "access": "TOKEN_ACCESS"
}
```

## Zarządzanie zadaniami
### Dodanie nowego zadania
```sh
curl -X POST "http://localhost:8000/tasks/create/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer TOKEN_ACCESS" \
    -d '{"name": "New Task", "description": "Task details", "status": "new", "assigned_to": 1}'
```
**Odpowiedź:**
```json
{
    "id": 1,
    "name": "New Task",
    "description": "Task details",
    "status": "new",
    "assigned_to": 1
}
```
### Pobranie wszystkich zadań (z możliwością filtracji)
```sh
curl -X GET "http://localhost:8000/tasks/" 
```
**Odpowiedź:**
```json
[
    {
        "id": 1,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "assigned_to": 1
    }
]
```
### Pobranie konkretnego zadania
```sh
curl -X GET "http://localhost:8000/tasks/1/" -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
```json
{
    "id": 1,
    "name": "New Task",
    "description": "Task details",
    "status": "new",
    "assigned_to": 1
}
```
### Pobranie listy zadań przypisanych do aktualnie zalogowanego usera
```sh
curl -X GET "http://localhost:8000/user-tasks/" -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
```json
[
    {
        "id": 3,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "assigned_to": 3
    }
]
```
### Pobieranie listy zadań przypisanych do konkretnego usera (tylko admin)
```sh
curl -X GET "http://localhost:8000/tasks/user/3/" -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
```json
[
    {
        "id": 3,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "assigned_to": 3
    }
]
```
### Edycja zadania
```sh
curl -X PUT "http://localhost:8000/tasks/10/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer TOKEN_ACCESS" \
    -d '{"name": "New Task", "description": "Edited task details", "status": "new", "assigned_to": 1}'
```
**Odpowiedź:**
```json
{
    "id": 1,
    "name": "New Task",
    "description": "Edited task details",
    "status": "new",
    "assigned_to": 1
}
```
### Usunięcie zadania
```sh
curl -X DELETE 'http://localhost:8000/tasks/1/' \
    -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
```json
{
    "detail": "You do not have permission to perform this action."
}
```
Tylko admin może usuwać zadania z bazdy danych, wykonajmy tą samą komendę z tokenem admina
```sh
curl -X DELETE 'http://localhost:8000/tasks/1/' \
    -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
Status 204 No Content (brak treści)

## Historia zadań
### Pobieranie historii ( z możliwością filtracji)
```sh
curl -X GET 'http://localhost:8000/history/' \
    -H "Authorization: Bearer TOKEN_ACCESS"
```
**Odpowiedź:**
```json
[
    {
        "id": 5,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "action_type": "created",
        "changed_at": "2025-04-09T14:14:37.933332Z",
        "task": 3,
        "assigned_to": 3,
        "changed_by": 3
    },
    {
        "id": 4,
        "name": "New Task",
        "description": "Edited task details",
        "status": "new",
        "action_type": "updated",
        "changed_at": "2025-04-09T14:11:03.553543Z",
        "task": 2,
        "assigned_to": 1,
        "changed_by": 3
    },
    {
        "id": 3,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "action_type": "created",
        "changed_at": "2025-04-09T14:10:32.192358Z",
        "task": 2,
        "assigned_to": 1,
        "changed_by": 3
    }
]
```
## Filtrowanie historii i zadań
### Zadania przypisane do danego użytkownika
```sh
curl -X GET 'http://localhost:8000/tasks/?id=&name__icontains=&description__icontains=&status=&assigned_to=1'
```
**Odpowiedź:**
```json
[
   {
        "id": 2,
        "name": "New Task",
        "description": "Edited task details",
        "status": "new",
        "assigned_to": 1
    }
]
```
### Zadania które mają w nazwie 'task' bez względu na wielkość liter
```sh
curl -X GET 'http://localhost:8000/tasks/?id=&name__icontains=task&description__icontains=&status=&assigned_to='
```
**Odpowiedź:**
```json
[
    {
        "id": 2,
        "name": "New Task",
        "description": "Edited task details",
        "status": "new",
        "assigned_to": 1
    },
    {
        "id": 3,
        "name": "New Task",
        "description": "Task details",
        "status": "resolved",
        "assigned_to": 3
    }
]
```
### Zadania które mają status "Nowy"
```sh
curl -X GET 'http://localhost:8000/tasks/?id=&name__icontains=&description__icontains=&status=new&assigned_to='
```
**Odpowiedź:**
```json
[
    {
        "id": 2,
        "name": "New Task",
        "description": "Edited task details",
        "status": "new",
        "assigned_to": 1
    }
]
```
### Historia zmian dla zadania o id=2
```sh
curl -X GET 'http://localhost:8000/history/?task=2&name__icontains=&assigned_to=&changed_by=&changed_at__gte=&changed_at__lte='
```
**Odpowiedź:**
```json
[
    {
        "id": 4,
        "name": "New Task",
        "description": "Edited task details",
        "status": "new",
        "action_type": "updated",
        "changed_at": "2025-04-09T14:11:03.553543Z",
        "task": 2,
        "assigned_to": 1,
        "changed_by": 3
    },
    {
        "id": 3,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "action_type": "created",
        "changed_at": "2025-04-09T14:10:32.192358Z",
        "task": 2,
        "assigned_to": 1,
        "changed_by": 3
    }
]
```
### Historia zadań przypisanych userowi o id=3
```sh
curl -X GET 'http://localhost:8000/history/?task=&name__icontains=&assigned_to=3&changed_by=&changed_at__gte=&changed_at__lte='
```
**Odpowiedź:**
```json
[
    {
        "id": 5,
        "name": "New Task",
        "description": "Task details",
        "status": "new",
        "action_type": "created",
        "changed_at": "2025-04-09T14:14:37.933332Z",
        "task": 3,
        "assigned_to": 3,
        "changed_by": 3
    }
]
```
