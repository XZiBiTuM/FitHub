$(document).ready(function() {
    $('#add-to-cart-button').click(function() {
        const form = $('#cart-form');
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            success: function(data) {
                console.log(data);
                $('#cart-button').click();
            },
            error: function(xhr, errmsg, err) {
                console.error('Ошибка:', errmsg, err);
                alert('Ошибка при добавлении товара в корзину.');
            }
        });
    });
});
