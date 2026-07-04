from __future__ import annotations

from celery import Celery

from app.core.config import settings

if not settings.celery_broker_url or not settings.celery_result_backend:
    raise RuntimeError(
        "Celery is not configured. Set CELERY_BROKER_URL and CELERY_RESULT_BACKEND to run workers."
    )

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "heartbeat-every-minute": {
            "task": "app.workers.tasks.heartbeat",
            "schedule": 60.0,
        }
    },
)

if __name__ == "__main__":
    # Allows: python -m app.workers.celery_app worker/beat ...
    celery_app.start()

