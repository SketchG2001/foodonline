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
    // Initialize quantity values on page load
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        console.log('Setting initial qty for', the_id, 'to', qty);  // Log the details
        $('#' + the_id).html(qty);
    });

    // Add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');
        var data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required'){
                    Swal.fire(response.message, '','info').then(function (){
                        window.location = '/login';
                    });
                } else if (response.status == 'Failed'){
                    Swal.fire(response.message, '', 'error');
                } else {
                    var cart_count = response.cart_counter['cart_count'];
                    $('#card_counter').html(cart_count);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        });
    });

    // Decrease cart
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status == 'login_required'){
                    Swal.fire(response.message, '','info').then(function (){
                        window.location = '/login';
                    });
                } else if (response.status == 'Failed'){
                    Swal.fire(response.message, '', 'error');
                } else {
                    var cart_count = response.cart_counter['cart_count'];
                    $('#card_counter').html(cart_count);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        });
    });
});

