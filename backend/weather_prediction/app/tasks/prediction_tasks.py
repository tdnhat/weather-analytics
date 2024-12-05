import os
import ssl
import asyncio
from celery import Celery
from redis import Redis
from celery.schedules import crontab
from ..config.settings import settings
from ..config.logging import logger
from celery.signals import worker_ready, worker_shutdown
from ..schedulers.prediction_schedulers import WeatherPredictionScheduler

# Initialize Redis client
redis_client = Redis.from_url(
    settings.REDIS_URL,
    ssl_cert_reqs=ssl.CERT_NONE
)

celery_app = Celery('weather_prediction',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
)

scheduler = WeatherPredictionScheduler(is_worker=settings.CELERY_WORKER)

@worker_shutdown.connect
def cleanup(sender, **kwargs):
    if scheduler.consumers:
        for consumer in scheduler.consumers.values():
            consumer.close()

@celery_app.task(name="app.tasks.prediction_tasks.process_training_prediction_model")
def process_training_prediction_model():
    logger.info("Bắt đầu task training model")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_training_model())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task training model: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

@worker_ready.connect
def at_start(sender, **kwargs):
    logger.info("Worker đã sẵn sàng - Bắt đầu chạy các task ban đầu")
    if settings.PREDICTION_TRAINING_ENABLED:
        process_training_prediction_model.delay()

# Cấu hình schedule cho các task
beat_schedule = {}

if settings.PREDICTION_TRAINING_ENABLED:
    beat_schedule['prediction_training'] = {
        'task': 'app.tasks.prediction_tasks.process_training_prediction_model',
        'schedule': settings.PREDICTION_TRAINING_SCHEDULE,
        'options': {'queue': 'prediction_tasks'}
    }

celery_app.conf.beat_schedule = beat_schedule
celery_app.conf.task_routes = {'app.tasks.prediction_tasks.*': {'queue': 'prediction_tasks'}}