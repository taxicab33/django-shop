from shop_main.models import *
from shop_main.services import create_sorting_list, compare_props_values, get_products_with_props_values, \
    manage_product_list_params


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

    def product_list(self):
        """Filtering queryset by request's params"""
        cat = Category.objects.get(slug=self.kwargs['cat_slug'])
        params_list = dict(self.request.GET)
        return manage_product_list_params(params_list, cat)

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
