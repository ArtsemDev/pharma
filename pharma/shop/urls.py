from django.urls import path

from .views import *


urlpatterns = [
    path('', ProductListView.as_view(), name='shop_product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='shop_product_detail')
]
