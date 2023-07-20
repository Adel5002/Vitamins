from django.urls import path

from .views import ProdictList, ProductDetails, AddComment

# app_name = 'Vitamins'

urlpatterns = [
    path('', ProdictList.as_view(), name='main'),
    path('<slug:slug>/', ProductDetails.as_view(), name='product_details'),
    path('comments/<slug:slug>/', AddComment.as_view(), name='add_comment'),
]