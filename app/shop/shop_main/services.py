from shop_main.models import CategoryPropertyValue, Product


def create_sorting_list():
    sort_dict = []
    price_sort = {'name': 'Цена', 'asc': 'price', 'desc': '-price'}
    sort_dict.append(price_sort)
    # rating_sort = {'name': 'Рейтинг', 'asc': 'rating', 'desc': '-rating'}
    # sort_dict.append(rating_sort)
    # popularity_sort = {'name': 'Популярность', 'asc': 'popularity', 'desc': '-popularity'}
    # sort_dict.append(popularity_sort)
    name_sort = {'name': 'Имя', 'asc': 'name', 'desc': '-name'}
    sort_dict.append(name_sort)
    return sort_dict


def compare_props_values(params_list, cat):
    # значения характеристик в параметрах запроса
    req_props_values = CategoryPropertyValue.objects.filter(property__name__in=params_list.keys(),
                                                            product__cat=cat)
    # значение всех характеристик продуктов, имеющих значения характеристик в параметрах запроса
    products_all_values = CategoryPropertyValue.objects.filter(product__in=req_props_values.values('product'))
    # проверяем наличие параметра сортировки
    not_filtered_products = get_products_with_props_values(params_list, req_props_values)
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


def get_products_with_props_values(params_list, req_props_values):
    """Gets products with props and value from params_list"""
    if params_list.get('sort'):
        not_filtered_products = Product.objects.filter(pk__in=req_props_values.values('product')) \
            .order_by(params_list.get('sort')[0])
        # удаляем параметр сортировки из словаря, чтобы он не мешал при фильтрации
        params_list.pop('sort')
    else:
        not_filtered_products = Product.objects.filter(pk__in=req_props_values.values('product'))

    return not_filtered_products


def manage_product_list_params(params_list, cat):
    """Manage params_list for queryset"""
    sort_param = ''
    # проверяем наличие праметра сортировки
    if params_list.get('sort'):
        sort_param = params_list.get('sort')[0]
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
        products = compare_props_values(params_list, cat)

    return products