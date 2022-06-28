from django.contrib import admin
from shop_main.models import *


admin.site.register(Category)
admin.site.register(CategoryProperty)
admin.site.register(CategoryPropertyValue)
admin.site.register(Product)