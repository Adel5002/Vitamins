from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404

from .models import Product, Comment
from .forms import CommentForm


class ProdictList(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'



class ProductDetails(DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_rating = Comment.objects.filter(product=self.object).aggregate(rating=Avg('rating'))

        context['avg_rating'] = avg_rating
        return context


class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'


    def form_valid(self, form):
        form.instance.product = Product.objects.get(slug=self.kwargs['slug'])
        form.instance.commentator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_details', kwargs={'slug': self.object.product.slug})

