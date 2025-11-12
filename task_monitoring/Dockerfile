FROM python:3.12

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--timeout", "600", "task_monitoring.wsgi"]
