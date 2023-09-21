import json
import uuid
import os

from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Avg, F, Sum, Q, Count
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator


from yookassa import Configuration, Payment, Settings
from decimal import Decimal

from .payment_acceptance import payment_acceptance
from .cart import Cart
from .models import Product, Comment, Category, CartOrderItem
from .forms import CommentForm, CartAddProductForm, CartSubtractProductForm, OrderCreateForm, CartOrder
from .mixins import SuperuserRequiredMixin



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
    comments_paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_rating = Comment.objects.filter(product=self.object).aggregate(rating=Avg('rating'))
        cart_product_form = CartAddProductForm()
        comments = Comment.objects.filter(product=self.object).order_by('id')
        paginator = Paginator(comments, self.comments_paginate_by)
        page_number = self.request.GET.get('page')
        com_form = CommentForm

        context['com_form'] = com_form
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
    paginate_by = 3

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
    template_name = 'product_details.html'

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
        cart.add(product=product, quantity=quantity)
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


Configuration.configure_auth_token(os.getenv('AUTH_TOKEN'))

settings = Settings.get_account_settings()


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            orders = form.save(commit=False)
            orders.user = request.user
            order = form.save()

            cart_items = list(cart)

            for item in cart_items:
                product = get_object_or_404(Product, slug=item['product'].slug)
                if product.quantity >= item['quantity']:
                    CartOrderItem.objects.create(order=order,
                                                 product=item['product'],
                                                 price=item['price'],
                                                 qty=item['quantity'])
                    product.quantity -= item['quantity']
                    product.save()
                if product.quantity == 0:
                    product.is_available = False
                    product.save()
                else:
                    pass

            cart.clear()
            order_id = CartOrder.objects.filter(user=request.user).last().id
            total = sum(Decimal(item['price']) * item['quantity'] for item in cart_items)
            payment = Payment.create({
                "amount": {
                    "value": total,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"{os.getenv('CSRF_TRUSTED_ORIGINS')}/order_succeeded"
                },
                "metadata": {
                    'order_id': order_id,
                },
                "capture": True,
                "description": f'Ваш номер заказа {order_id}'
                }, uuid.uuid4())
            return HttpResponseRedirect(payment.confirmation.confirmation_url)

    else:
        form = OrderCreateForm

    return render(request, 'order/create.html',
                  {'cart': cart, 'form': form})


class Webhooks(ListView):
    template_name = 'webhooks.html'
    model = CartOrder

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)
        if payment_acceptance(response):
            return HttpResponse(200)
        return HttpResponse(404)


class OrderAcceptance(ListView):
    template_name = 'order/order_acceptance.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = CartOrder.objects.filter(user=self.request.user).last()
        return queryset


class UserOrders(ListView):
    template_name = 'user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = CartOrder.objects.filter(user=self.request.user).order_by('-id')[:3]
        return queryset


class PageNotFoundErrorView(TemplateView):
    template_name = 'exceptions/404.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)


class ServerErrorView(TemplateView):
    template_name = 'exceptions/500.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=500)


class Chart(SuperuserRequiredMixin, ListView):
    model = CartOrderItem
    template_name = 'charts/chart.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = CartOrderItem.objects.filter(order__paid=True).values('product__title').annotate(
            qt=Sum('qty'))
        print(queryset)
        return queryset

