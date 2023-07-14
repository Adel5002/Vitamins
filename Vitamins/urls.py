from django.urls import path

from .views import ProdictList, ProductDetails

# app_name = 'Vitamins'

urlpatterns = [
    path('', ProdictList.as_view(), name='main'),
    path('<slug:slug>/', ProductDetails.as_view(), name='product_details')
]