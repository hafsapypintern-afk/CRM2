import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Order


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_saved(sender, instance, created, **kwargs):

    if created:

        logger.info(
            f"Order {instance.id} created"
        )

    else:

        logger.info(
            f"Order {instance.id} updated"
        )


@receiver(post_delete, sender=Order)
def order_deleted(sender, instance, **kwargs):

    logger.info(
        f"Order {instance.id} deleted"
    )