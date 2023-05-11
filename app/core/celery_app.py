from celery import Celery

from app.core.config import settings

# Initialize Celery with a Redis broker and JSON serializer
celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_default_queue = "app_tasks"
