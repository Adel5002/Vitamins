from django.urls import path

from .views import index

# app_name = 'Vitamins'

urlpatterns = [
    path('', index, name='index')
]