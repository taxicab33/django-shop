from django.db.models import Q

from shop_main.models import *
from shop_main.services import create_sorting_list


class DataMixin:
    paginate_by = 2

    @classmethod
    def get_categories(cls, **kwargs):
        """Get all categories"""
        cats = Category.objects.all()
        return cats

    @classmethod
    def get_values(cls, filters_list):
        """Gets values of request's params dict"""
        values = []
        for spisok in list(filters_list.values()):
            for sub_value in spisok:
                values.append(sub_value)
        return values

    @classmethod
    def filter_product_list(cls, params_list, cat):
        # значения характеристик в параметрах запроса
        req_props_values = CategoryPropertyValue.objects.filter(property__name__in=params_list.keys(),
                                                                product__cat=cat)
        # значение всех характеристик продуктов, имеющих значения характеристик в параметрах запроса
        products_all_values = CategoryPropertyValue.objects.filter(product__in=req_props_values.values('product'))
        # проверяем наличие параметра сортировки
        if params_list.get('sort'):
            not_filtered_products = Product.objects.filter(pk__in=req_props_values.values('product'))\
                .order_by(params_list.get('sort')[0])
            # удаляем параметр сортировки из словаря, чтобы он не мешал при фильтрации
            params_list.pop('sort')
        else:
            not_filtered_products = Product.objects.filter(pk__in=req_props_values.values('product'))

        products = []

        for product in not_filtered_products:
            # формируем словарь характеристик для каждого продукта
            product_prop_value_dict = {}
            for product_prop_value in products_all_values:
                if product_prop_value.product == product:
                    prop_value = {f'{product_prop_value.property.name}': product_prop_value.value}
                    product_prop_value_dict.update(prop_value)
            # сравниваем со списком фильтров
            coincidence = 0
            for key, values in params_list.items():
                if product_prop_value_dict.get(key) in values:
                    coincidence += 1
            # кол-во совпадений должно быть равно кол-ву параметров фильтрации в запросе
            if coincidence == len(params_list): products.append(product)

        return products

    def product_list(self):
        """Filter queryset by request's params"""
        cat = Category.objects.get(slug=self.kwargs['cat_slug'])
        params_list = dict(self.request.GET)
        sort_param = ''
        # проверяем наличие праметра сортировки
        if dict(self.request.GET).get('sort'):
            sort_param = dict(self.request.GET).get('sort')[0]
        # проверяем наличие номера текущей страницы пагинатора и удаляем, чтобы не мешался
        if 'page' in params_list:
            params_list.pop('page')
        # если параметры запроса отсутсвуют
        if not params_list:
            products = Product.objects.filter(cat=cat)
        # если присутсвует только параметр сортировки
        elif sort_param and len(params_list) == 1:
            products = Product.objects.filter(cat=cat).order_by(sort_param)
        # если присутсвует параметры фильтрации (и сортировки)
        else:
            products = self.filter_product_list(params_list, cat)

        return products

    def get_products_list_context(self, context):
        """Gets nessesary data for category listview"""
        context['category'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['title'] = context['category']
        params_list = dict(self.request.GET)
        if 'page' in params_list:
            params_list.pop('page')
        if params_list.get('sort'):
            context['picked_sort_param'] = params_list.get('sort')[0]
        context['picked_filters'] = params_list
        # cats - категории
        context['cats'] = self.get_categories()
        context['category_props'] = CategoryProperty.objects.filter(category=context['category'].pk)
        context['category_props_values'] = CategoryPropertyValue.objects.filter(property__in=context['category_props'])\
            .order_by('value').distinct('value')
        context['sorting_list'] = create_sorting_list()
        return context

    def get_product_context(self, context):
        """Get nessesary data for product detailview"""
        context['cats'] = self.get_categories(category=context['product'].name)
        context['title'] = context['product']
        context['props'] = CategoryProperty.objects.filter(category=context['product'].cat)
        context['props_value'] = CategoryPropertyValue.objects.filter(product=context['product'])
        return context