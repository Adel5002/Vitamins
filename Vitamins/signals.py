from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import CartOrder

@receiver(post_save, sender=CartOrder)
def notify_admin_abt_new_payment(sender, instance, created, **kwargs):
    template = None

    if instance.paid:
        print('Im paid order!!!')
        first_name = instance.first_name
        last_name = instance.last_name
        user_email = instance.email
        address = instance.address
        postal_code = instance.postal_code
        products = [f'{product.qty}x {product.product.title}' for product in instance.cartorderitem_set.all()]
        total_price = [int(product.get_cost()) for product in instance.cartorderitem_set.all()]
        subject = 'Новый оплаченный заказ!'

        email = settings.ADMIN
        template = 'html_messages/paid_order.html'
    else:
        return

    html_content = render_to_string(
        f'{template}',
        {
            'first_name': first_name,
            'last_name': last_name,
            'user_email': user_email,
            'address': address,
            'postal_code': postal_code,
            'products': ', '.join(products),
            'total_price': sum(total_price)
        }
    )

    message = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    print(email)
    message.attach_alternative(html_content, 'text/html')
    message.send()
