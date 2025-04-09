FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./task_manager/ /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_manager.wsgi:application"]