// Получение переменной cookie по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function open_catalog(){
    var catalog = document.getElementById('catalog');
    if (catalog.classList.contains("open-catalog")) {
        catalog.classList.remove('open-catalog');
        document.querySelector('.catalog-btn').textContent = "Каталог";
    }
    else{
        catalog.classList.add('open-catalog');
        document.querySelector('.catalog-btn').textContent = "Закрыть";
    }
}

function show_sub_categories(){
    var main_cat = $(this)
    var parent_id = main_cat.attr('id')
    var sub_cat_list = document.querySelectorAll('.sub-cat-list')
    for (i = 0; i < sub_cat_list.length; i++){
        if(sub_cat_list[i].id == 'parent-'+parent_id){
            sub_cat_list[i].classList.remove('d-none')
        }
        else{
            sub_cat_list[i].classList.add('d-none')
        }
    }
    var main_cat_list = document.querySelectorAll('.main-category')
    for (i = 0; i < main_cat_list.length; i++){
        if(main_cat_list[i].id == parent_id){
            main_cat_list[i].classList.add('active-btn')
        }
        else{
            main_cat_list[i].classList.remove('active-btn')
        }
    }
}

function doSubmit(id){
    f = document.getElementById(id);
    f.submit();
    }

$(function() {
    $('.catalog-btn').click(open_catalog);
    $('#catalog').mouseleave(open_catalog);
    $('.main-category').mouseenter(show_sub_categories);
});