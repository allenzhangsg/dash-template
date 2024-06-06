from celery import Celery

celery_app = Celery(loader="", backend="")
