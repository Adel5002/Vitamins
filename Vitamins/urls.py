from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from .views import ProdictList, ProductDetails, AddComment, cart_detail, cart_add, cart_remove, CategoryListView, \
    cart_subtract, SearchProducts, AboutUs, order_create, Webhooks, OrderAcceptance, UserOrders, cart_update_quantity, \
    Chart


# app_name = 'Vitamins'

urlpatterns = [
    path('', ProdictList.as_view(), name='main'),
    path('search/', SearchProducts.as_view(), name='search_results'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
    path('<slug:slug>/', ProductDetails.as_view(), name='product_details'),
    path('comments/<slug:slug>/', AddComment.as_view(), name='add_comment'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_products'),

    path('cart_detail', cart_detail, name='cart_detail'),
    path('cart_detail/add/<slug:product_slug>/', cart_add, name='cart_add'),
    path('cart_detail/update/<slug:product_slug>/', cart_update_quantity, name='cart_update'),
    path('cart_detail/subtract/<slug:product_slug>/', cart_subtract, name='cart_subtract'),
    path('cart_detail/remove/<slug:product_slug>/', cart_remove, name='cart_remove'),

    path('create', order_create, name='order_create'),
    path('webhooks', csrf_exempt(Webhooks.as_view())),
    path('order_succeeded', OrderAcceptance.as_view()),
    path('user_orders', UserOrders.as_view(), name='user_orders'),

    path('chart', Chart.as_view(), name='chart')
]