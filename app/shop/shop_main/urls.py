from django.urls import path

from shop_main.views import Main, ShowCategory, ShowProduct

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='cat'),
    path('product/<slug:product_slug>', ShowProduct.as_view(), name='product'),
]

