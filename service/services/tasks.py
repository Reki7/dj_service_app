import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription
    # subscription = Subscription.objects.get(id=subscription_id)

    time.sleep(10)

    subscription = Subscription.objects.filter(id=subscription_id).annotate(annotated_price=F('service__full_price') -
                                                                                  F('service__full_price') *
                                                                                  F('plan__discount_percent') / 100
                                                                            ).first()
    subscription.price = subscription.annotated_price
    # new_price = subscription.service.full_price - subscription.service.full_price * subscription.plan.discount_percent / 100
    # subscription.price = new_price
    # subscription.save(save_model=False)
    subscription.save()