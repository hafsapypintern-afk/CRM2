import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, created, **kwargs):

    if created:
        logger.info(
            f"Customer {instance.id} created"
        )
    else:
        logger.info(
            f"Customer {instance.id} updated"
        )