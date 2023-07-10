from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Vendor(models.Model):
    name = models.CharField()


class Product(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text='Указывать не обяз \
                                                                                 ательно, это просто задел на будущее!')

    price = models.DecimalField(max_digits=99999999999, decimal_places=2)
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, null=True, blank=True, help_text='Указ\
                                            ывать в том случае если хотите сделать скидку')

    image = models.ImageField(upload_to='vitamins/')
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, db_index=True)
    specifications = models.TextField()
    is_available = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['dateCreation']


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    product = models.ManyToManyField(Product)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
