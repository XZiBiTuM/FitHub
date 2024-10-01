$(document).ready(function() {
    $('#cart-button').on('click', function() {
        $('#cart-sidebar').toggleClass('show');

        if ($('#cart-sidebar').hasClass('show')) {
            loadCart();
        }
    });

    function loadCart() {
        $.ajax({
            url: '/cart/',
            type: 'GET',
            success: function(data) {
                $('#cart-sidebar-content').html(data);
            }
        });
    }

    $('#cart-sidebar-content').on('click', '.update-cart', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var action = $(this).data('action');

        $.ajax({
            url: '/update_cart_quantity/' + productId + '/' + action + '/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            success: function(data) {
                updateCart(data);
            }
        });
    });

    $('#cart-sidebar-content').on('click', '.remove-from-cart', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');

        $.ajax({
            url: '/remove_from_cart/' + productId + '/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            success: function(data) {
                updateCart(data);
            }
        });
    });

    $('#cart-sidebar-content').on('click', '#order-button', function(e) {
        e.preventDefault();

        $.ajax({
            url: '/order/',
            type: 'GET',
            success: function(data) {
                $('#cart-sidebar-content').html(data);
            }
        });
    });

    $('#cart-sidebar-content').on('submit', '#order-form', function(e) {
        e.preventDefault();

        var checkStockUrl = $('#order-form').data('check-stock-url');

        $.ajax({
            url: checkStockUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            success: function(data) {
                if (data.status === 'ok') {
                    $.ajax({
                        url: $('#order-form').attr('action'),
                        type: 'POST',
                        data: $('#order-form').serialize(),
                        headers: {
                            'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
                        },
                        success: function(response) {
                            if (response.status === 'ok') {
                                $.ajax({
                                    url: '/order_success/',
                                    type: 'GET',
                                    success: function(data) {
                                        $('#cart-sidebar-content').html(data);
                                    }
                                });
                            } else if (response.status === 'error') {
                                alert(response.message);
                            }
                        }
                    });
                } else {
                    var message = 'Недостаточное количество следующих товаров:\n';
                    $.each(data.insufficient_stock, function(index, item) {
                        message += item.title + ': запрошено ' + item.requested_quantity + ', доступно ' + item.available_quantity + '\n';
                    });
                    alert(message);
                }
            }
        });
    });

    function updateCart(data) {
        var cartContent = '';
        $.each(data.cart_items, function(index, item) {
            cartContent += '<li data-product-id="' + item.id + '">';
            cartContent += item.title + ' - ' + item.quantity + ' шт. - ' + item.total_price + ' руб.';
            cartContent += '<button class="update-cart" data-action="increase" data-product-id="' + item.id + '">+</button>';
            cartContent += '<button class="update-cart" data-action="decrease" data-product-id="' + item.id + '">-</button>';
            cartContent += '<button class="remove-from-cart" data-product-id="' + item.id + '">Удалить</button>';
            cartContent += '</li>';
        });
        $('#cart-content ul').html(cartContent);
        $('#total-price').text(data.total_price);
    }
});
