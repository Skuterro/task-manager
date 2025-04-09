#### 1.Budowanie projektu 
za pomocą runserver
```sh
docker compose -f docker-compose.yml up --build
```
za pomocą gunicorn
```sh
docker compose -f docker-compose.guni.yml up --build
```
### 1.1 Jeżeli projekt budowany jest pierwszy raz, po uruchomieniu bazy danych należy wywołać
```sh
docker exec -it task_manager-api-1 python manage.py makemigrations                                    
docker exec -it task_manager-api-1 python manage.py migrate
```
Dostęp do aplikacji
```
http://localhost:8000/
```
