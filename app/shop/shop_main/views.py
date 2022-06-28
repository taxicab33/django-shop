from django.views.generic import ListView, DetailView
from shop_main.models import *
from shop_main.utils import DataMixin


class Main(DataMixin, ListView):
    model = Product
    template_name = 'shop_main/main.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cats'] = self.get_categories()
        return context


class ShowCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop_main/categories.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        return self.product_list()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_products_list_context(context)
        return context


class ShowProduct(DetailView, DataMixin):
    model = Product
    template_name = 'shop_main/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_product_context(context)
        return context
