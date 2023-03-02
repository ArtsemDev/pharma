from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product


class ProductListView(ListView):
    template_name = 'shop/shop.html'
    model = Product
    paginate_by = 3


class ProductDetailView(DetailView):
    template_name = 'shop/shop-single.html'
    model = Product
