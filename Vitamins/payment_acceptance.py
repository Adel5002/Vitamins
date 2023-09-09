from.models import CartOrder


def payment_acceptance(response, cartorder_id):
    if response['event'] == 'payment.succeeded':
        payment = CartOrder.objects.get(id=cartorder_id)
        payment.paid = True
        payment.save()
    elif response['event'] == 'payment.canceled':
        print('Payment was canceled')
    return True

