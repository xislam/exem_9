const baseUrl = 'http://localhost:8000/api/';



function like(id) {
    // var like = $(this);
    // var type = like.data('type');
    // var pk = like.data('id');
    // var action = like.data('action');
    // var dislike = like.next();

    $.ajax({
        url: "/api/" + id + '/like' + "/",
        type: 'POST',
        data: {'obj': id},

        success: function () {
            let likeHtml = $('#like_span_' + id);
            let numLike = likeHtml.text();
            let objLike = parseInt(numLike) + 1;
            likeHtml.text(objLike)
        },
        error: function (response, status) {
            console.log('no', id);
        }
    });

    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url: "/api/type/id/action/",
        type: 'POST',
        data: {'obj': pk},

        success: function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

// Подключение обработчиков
// $(function () {
//     $('[data-action="like"]').click(like);
//     $('[data-action="dislike"]').click(dislike);
// });


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