from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
import os
import glob
from app.settings import BASE_DIR


@shared_task(rate_limit='10/m')
def send_notify(instance_id):
    from .models import CartOrder
    try:
        instance = CartOrder.objects.get(id=instance_id)
        if instance.paid:
            order_id = instance_id
            first_name = instance.first_name
            last_name = instance.last_name
            user_email = instance.email
            address = instance.address
            city = instance.city
            postal_code = instance.postal_code
            products = [f'{product.qty}x {product.product.title}' for product in instance.cartorderitem_set.all()]
            total_price = [int(product.get_cost()) for product in instance.cartorderitem_set.all()]
            phone_number = instance.phone_number
            subject = 'Новый оплаченный заказ!'

            email = settings.ADMIN
            template = 'html_messages/paid_order.html'

        else:
            return

        html_content = render_to_string(
            f'{template}',
            {
                'order_id': order_id,
                'first_name': first_name,
                'last_name': last_name,
                'user_email': user_email,
                'address': address,
                'city': city,
                'postal_code': postal_code,
                'products': ', '.join(products),
                'total_price': sum(total_price),
                'phone_number': phone_number
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
    except Exception:
        pass


@shared_task
def delete_not_actual_caches():
    cache_folder = os.path.join(BASE_DIR, "site_cache")
    caches = glob.glob(os.path.join(cache_folder, "*.djcache"))

    for cache_file in caches:
        try:
            os.unlink(cache_file)
        except OSError as e:
            print("Error: %s: %s" % (cache_file, e.strerror))




