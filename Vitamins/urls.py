from django.urls import path

from .views import ProdictList, ProductDetails, AddComment, cart_detail, cart_add, cart_remove

# app_name = 'Vitamins'

urlpatterns = [
    path('', ProdictList.as_view(), name='main'),
    path('<slug:slug>/', ProductDetails.as_view(), name='product_details'),
    path('comments/<slug:slug>/', AddComment.as_view(), name='add_comment'),

    path('cart_detail', cart_detail, name='cart_detail'),
    path('cart_detail/add/<slug:product_slug>/', cart_add, name='cart_add'),
    path('cart_detail/remove/<slug:product_slug>/', cart_remove, name='cart_remove'),
]