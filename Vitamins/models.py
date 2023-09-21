from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from unidecode import unidecode


STATUS_CHOICE = (
    ('process', 'В процессе'),
    ('shipped', 'Отправлено'),
    ('Delivered', 'Доставлено'),
)


RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)


class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    slug = models.SlugField('Слаг', unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'


class Vendor(models.Model):
    name = models.CharField('Название', max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Производитель'



class Product(models.Model):
    categories = models.ForeignKey( Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text='Указывать не обяз \
                                                                                 ательно, это просто задел на будущее!')

    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    old_price = models.DecimalField('Старая цена', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Указ\
                                            ывать в том случае если хотите сделать скидку')

    image = models.ImageField('Изображение', upload_to='vitamins/')
    title = models.CharField('Название продукта', max_length=120)
    description = models.TextField('Описание', null=True, blank=True)
    dateCreation = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', null=True, blank=True)
    slug = models.SlugField('Слаг', unique=True, db_index=True)
    specifications = models.TextField('Состав')
    release_form = models.CharField('Форма выпуска', max_length=120, null=True)
    age = models.PositiveSmallIntegerField('Возраст', null=True)
    country = models.CharField('Страна производитель', max_length=120, null=True)
    is_available = models.BooleanField('В наличии', default=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField('Количество', default=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})


    class Meta:
        ordering = ['dateCreation']
        verbose_name_plural = 'Добавление продукта'

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    images = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Кратинки к продукту'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING, default=None)

    class Meta:
        verbose_name_plural = 'Комментарии к продукту'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=250)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    city = models.CharField('Город', max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField('Статус платежа', default=False)
    phone_number = models.BigIntegerField('Номер телефона')
    track_number = models.CharField('Трекномер', max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

    def get_total_cost(self):
        orderitems = self.cartorderitem_set.all()
        total = sum([item.get_cost() for item in orderitems])
        return total

    def get_cart_item(self):
        orderitems = self.cartorderitem_set.all()
        total = sum([item.qty() for item in orderitems])
        return total


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_cost(self):
        return self.price * self.qty










