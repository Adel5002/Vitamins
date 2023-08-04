from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import QueryDict


from .cart import Cart
from .models import Product, Comment, Category, CartOrderItem
from .forms import CommentForm, CartAddProductForm, CartSubtractProductForm, OrderCreateForm




class ProdictList(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'
    comments_paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_rating = Comment.objects.filter(product=self.object).aggregate(rating=Avg('rating'))
        cart_product_form = CartAddProductForm()
        comments = Comment.objects.filter(product=self.object)
        paginator = Paginator(comments, self.comments_paginate_by)
        page_number = self.request.GET.get('page')

        context['comments'] = paginator.get_page(page_number)
        context['cart_product_form'] = cart_product_form
        context['avg_rating'] = avg_rating
        return context


class CategoryListView(ListView):
    model = Product
    template_name = 'products_by_categories.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return Product.objects.filter(categories=category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context


class SearchProducts(ListView):
    model = Product
    template_name = 'search_product.html'
    context_object_name = 'products'
    paginate_by = 2
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('title')
        if query:
            queryset = queryset.filter(title__iregex=query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        search_params = self.request.GET.copy()
        if 'page' in search_params:
            del search_params['page']

        context['search_params'] = search_params.urlencode()
        context['cart_product_form'] = cart_product_form
        return context


class AboutUs(TemplateView):
    template_name = 'about_us.html'


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



@require_POST
def cart_add(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_update_quantity(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        cart.update(product=product, quantity=quantity)

    return redirect('cart_detail')


def cart_subtract(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    form = CartSubtractProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.subtract(product=product,
                      quantity=cd['quantity'],
                      update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                CartOrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         qty=item['quantity'])

            # очистка корзины
            cart.clear()
            return render(request, 'order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order/create.html',
                  {'cart': cart, 'form': form})