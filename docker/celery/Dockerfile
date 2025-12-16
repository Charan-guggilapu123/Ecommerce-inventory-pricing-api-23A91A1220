FROM python:3.11-slim

WORKDIR /app

COPY requirements/base.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["celery", "-A", "config", "worker", "-l", "info"]
