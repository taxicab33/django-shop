
def create_sorting_list():
    sort_dict = []
    price_sort = {'name': 'Цена', 'asc': 'price', 'desc': '-price'}
    sort_dict.append(price_sort)
    rating_sort = {'name': 'Рейтинг', 'asc': 'rating', 'desc': '-rating'}
    sort_dict.append(rating_sort)
    popularity_sort = {'name': 'Популярность', 'asc': 'popularity', 'desc': '-popularity'}
    sort_dict.append(popularity_sort)
    name_sort = {'name': 'Имя', 'asc': 'name', 'desc': '-name'}
    sort_dict.append(name_sort)
    return sort_dict