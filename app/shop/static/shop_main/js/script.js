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

$(function() {
    $('body').on('click', '.catalog-btn', open_catalog);
    $('body').on('out', '#catalog'. open_catalog)
});