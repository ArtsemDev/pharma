from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Order, OrderItem


class ProductListView(ListView):
    template_name = 'shop/shop.html'
    model = Product
    paginate_by = 3
    #
    # def get_queryset(self):
    #     return self.model.filter(content__icontains=self.request.GET.get('q'))


class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shop/shop-single.html'
    model = Product
    login_url = '/login/'


class CartListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'shop/cart.html'
    context_object_name = 'order_item_list'

    def get_queryset(self):
        return self.model.objects.filter(
            Q(order__is_paid=False) & Q(order__user=self.request.user)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CartListView, self).get_context_data()
        context['total_amount'] = 0
        context['cart_amount'] = len(context[self.context_object_name])
        for product in context[self.context_object_name]:
            context['total_amount'] += product.product.price
        return context
