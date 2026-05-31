from celery import (
    shared_task,
)  # not from config.celery import app  ❌ (avoid), Import safety (rare issue)
from apps.common.services.email_service import send_email
import time
import logging

logger = logging.getLogger(__name__)

# @shared_task
# def send_product_creation_email(product_id):
#     print(f"Sending email for product {product_id}...")
#     time.sleep(5)  # simulate email sending delay
#     print(f"Email sent for product {product_id}!")


# retries on failure
# exponential delay
# max 3 retries
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_product_created_email(self, product_id, user_email):
    logger.info(f"Sending email for product {product_id}")
    send_email(
        subject="Product Created",
        to_email=user_email,
        template_name="emails/product_created.html",
        context={"product_id": product_id},
    )


# celery -A config worker --loglevel=info --pool=solo
# celery -A config beat --loglevel=info
@shared_task
def daily_product_report():
    print("Generating daily report...")
