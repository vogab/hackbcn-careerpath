from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request
from .tasks import process_request

@receiver(post_save, sender=Request)
def handle_request_save(sender, instance, created, **kwargs):
    if created:
        process_request(instance.id)
