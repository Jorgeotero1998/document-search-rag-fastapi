from __future__ import annotations

from app.core.logging import get_logger
from app.workers.celery_app import celery_app

log = get_logger(__name__)


@celery_app.task(name="app.workers.tasks.heartbeat")
def heartbeat():
    log.info("celery_heartbeat")
    return {"status": "ok"}

