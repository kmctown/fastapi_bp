import os
from celery import Celery


# Get Redis URL from environment variable or use default
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

# Initialize Celery with a Redis broker and JSON serializer
celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_default_queue = "app_tasks"
