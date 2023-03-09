from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='название',
        unique=True,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='название'
    )
    descr = models.CharField(
        max_length=4096,
        verbose_name='описание',
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='цена',
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='product/',
        null=True,
        blank=True
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique=True,
        null=False,
        blank=False
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    def get_absolute_url(self):
        return reverse('shop_product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Order {self.order} Product {self.product}'
