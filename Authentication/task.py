from celery import shared_task
from .views import ping_serverless

@shared_task
def periodic_ping():
    # Run the ping function periodically
    ping_serverless()

