from.models import CartOrder
from django.core.exceptions import ObjectDoesNotExist


def payment_acceptance(response):
    try:
        if response['event'] == 'payment.succeeded':
            payment = CartOrder.objects.get(
                id=response['object']['metadata']['order_id']
            )
            payment.paid = True
            payment.save()
        elif response['event'] == 'payment.canceled':
            print('Payment was canceled')
        return True
    except ObjectDoesNotExist:
        pass

