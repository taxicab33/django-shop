from time import time
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, verbose_name='URL')
    price = models.PositiveIntegerField(verbose_name='Цена', null=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    description = models.TextField(verbose_name="Описание товара", null=True)
    is_published = models.BooleanField(default=True, verbose_name='Видимость')
    image = models.ImageField(upload_to='products_images/', verbose_name='Изображение', default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, verbose_name='Сотрудник',
                             related_name='employee')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def get_properties(self):
        return CategoryPropertyValue.objects.filter(product=self)

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товар'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, verbose_name='URL')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', verbose_name="Изображение", blank=True)

    def save(self, *args, **kwargs):
        """При создании категории генерируем slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cat', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категории товаров"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_children(self):
        """Получаем всех потомков категории"""
        return Category.objects.filter(parent=self)

    def get_products(self):
        """Получаем все продукты категории"""
        products = Product.objects.filter(cat=self)
        if not self.get_children():
            products = Product.objects.filter(cat=self)
        else:
            for child in self.get_children():
                products = products.union(child.get_products())
        return products

    def products_exist(self):
        """Проверяем наличе хотябы 1 объекта категории"""
        products = Product.objects.filter(cat=self)[:1]
        if products.count() > 0:
            return True
        else:
            return False

    def get_parents(self):
        """Получаем список всех предков категории рекурсией"""
        parents = []
        if self.parent is not None:
            parents = parents + self.parent.get_parents()
        parents.append(self)
        return parents


class CategoryProperty(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Характеристика')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(verbose_name="Описание характеристики", null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="Слаг параметра", default="")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryPropertyValue(models.Model):
    value = models.CharField(max_length=255, verbose_name='Значение')
    property = models.ForeignKey('CategoryProperty', on_delete=models.CASCADE, verbose_name='Характеристика')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="Слаг значения параметра", default="")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения характеристик'
        ordering = ['product']

    def __str__(self):
        return self.property.name + ' ' + self.product.name

    # считаем кол-во товаров с данным значением
    def count_products(self):
        return CategoryPropertyValue.objects.filter(value=self.value, property=self.property).count()
