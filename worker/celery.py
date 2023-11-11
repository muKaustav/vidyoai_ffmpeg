from __future__ import absolute_import, unicode_literals
from celery import Celery
from decouple import config
import logging

logging.basicConfig(level=logging.INFO)


app = Celery("worker")

HOST_IP = config("HOST_IP")

app.conf.broker_url = "amqp://rabbitmq:5672"
app.conf.result_backend = "redis://redis:6379/0"

app.autodiscover_tasks(["worker.tasks"], force=True)

if __name__ == "__main__":
    logging.info("Starting Celery worker.")
    app.start()
