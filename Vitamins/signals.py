from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CartOrder
from .tasks import send_notify


@receiver(post_save, sender=CartOrder)
def notify_admin_abt_new_payment(sender, instance, created, **kwargs):
    template = None

    if instance.paid:
        send_notify.delay(instance.id)
