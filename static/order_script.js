        $('#back-to-cart').on('click', function() {
                $('#cart-sidebar').addClass('show');
                loadCart();
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