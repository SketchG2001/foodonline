let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['in']},
        })
// function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value
    geocoder.geocode({'address': address}, function (result, status) {
        // console.log('result=>',result);
        // console.log('status=>',status);
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = result[0].geometry.location.lat();
            var longitude = result[0].geometry.location.lng();
            // console.log('latitude=>', latitude,'longitude=>', longitude);
            if (latitude) {
                $('#id_latitude').val("");
                if ($('#id_latitude').val() === "") {
                    $('#id_latitude').val(latitude);
                }
            }
            if (longitude) {
                $('#id_longitude').val("");
                if ($('#id_longitude').val() === "") {
                    $('#id_longitude').val(longitude);
                }
            }
            $('#id_address').val(address);
        }
    });

    //     loop through the address component and assign the other address data
    // console.log(place.address_components)
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            //     get the country
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get the state
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get the city
            if (place.address_components[i].types[j] == 'locality') {
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get the pin code
            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_pin_code').val(place.address_components[i].long_name);
            } else {
                $('#id_pin_code').val("");
            }

        }
    }

}

// 2414E2A4822127 post office app

$(document).ready(function () {

    // add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    Swal.fire(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    });
                } else if (response.status == 'Failed') {
                    Swal.fire(response.message, '', 'error');

                } else {
                    var cart_count = response.cart_counter['cart_count']
                    $('#cart_counter').html(cart_count);
                    $('#qty-' + food_id).html(response.qty);
                    //     subtotal, tax, and granddtotal
                    applyCartamounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                }
            }
        })
    })
//     place the item quantity on load
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#qty-' + the_id).html(qty)
    })
//     decrease cart
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required') {
                    Swal.fire(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    });
                } else if (response.status == 'Failed') {
                    Swal.fire(response.message, '', 'error');
                } else {
                    var cart_count = response.cart_counter['cart_count']
                    $('#cart_counter').html(cart_count);
                    $('#qty-' + food_id).html(response.qty);
                    applyCartamounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }

                }
            }
        })
    })

//     Delete cart item
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'Failed') {
                    Swal.fire(response.message, '', 'error');
                } else {
                    var cart_count = response.cart_counter['cart_count']
                    $('#cart_counter').html(cart_count);
                    Swal.fire(response.message, '', 'success')
                    applyCartamounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    removeCartItem(0, cart_id);
                    checkEmptyCart();

                }
            }
        })
    })

//     Delete the cart element if the qty is 0
    function removeCartItem(cartItemQty, cart_id) {
        //     remove the cart item element

        if (cartItemQty <= 0) {
            document.getElementById("cart-item-" + cart_id).remove();
        }

    }

//     check if the cart is empty
    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerText;

        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block';
        }
    }

//     apply cart amounts
    function applyCartamounts(subtotal, tax, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#total').html(grand_total);
        }
    }

});