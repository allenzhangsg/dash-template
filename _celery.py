import logging
import os
from celery import Celery
from kombu import Exchange, Queue

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    logging.error("Trying to start app with celery, but no redis was found.\n"
                  "Add the redis url as environment variable `REDIS_URL`.")
    exit(-1)
else:
    logging.info(f"Using redis {REDIS_URL}")

celery_app = Celery(broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('production', Exchange('default'), routing_key='production'),  # for production deployments
    Queue('dev', Exchange('default'), routing_key='dev'),  # for dev deployments
)
celery_app.conf.task_default_exchange_type = 'direct'

DEPLOYENV = os.getenv("DEPLOYENV")
# isolate production and dev environments
if DEPLOYENV in ("Production", "Dev"):
    celery_app.conf.task_default_queue = DEPLOYENV.lower()
    celery_app.conf.task_default_routing_key = DEPLOYENV.lower()
else:
    celery_app.conf.task_default_queue = "default"
    celery_app.conf.task_default_routing_key = "default"
