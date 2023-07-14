from django.views.generic import DetailView, ListView

from .models import Product


class ProdictList(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'



class ProductDetails(DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'products'

