console.log("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH");

const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();
    let date = new Date();
    let time = date.getDay()+ " " + monthNames[date.getUTCMonth()] + ", " + date.getFullYear();
    $.ajax ({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("comment saved to db...");
            window.location.reload()

            if (response.bool == true){
                $("#review-response").html("Review Added Successfully.")
                $(".hide-comment-form").hide()
                $(".add-review-text").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+response.context.user+'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">'+time+'</span>'
                    _html += '</div>'

                    for(var i = 1; i <= response.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }

                    _html += '</div>'
                    _html += '<p class="mb-10">'+response.context.review+'</p>'
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html);
            }
        }
    })
})



$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox has been clicked");

        let filter_object = {}
        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            // console.log('filter key:', filter_key) 
            // console.log('filetr value:', filter_value)

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key+']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("filter object", filter_object);
        $.ajax({
            url: '/filter-product',
            data:  filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('Trying to filter products...');
            },
            success: function(response){
                console.log(response);
                console.log("Data filtered successfully");
                $("#filtered-products").html(response.data)
            }
        })
    })
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("current price:", current_price);
        // console.log("max price:", max_price);
        // console.log("min price:", min_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            min_price = Math.round(min_price*100)/100
            max_price = Math.round(max_price*100)/100

            alert("Price must be between GHC" + min_price + " and GHC" + max_price)
            $(this).val(min_price)
            $("#range").val(min_price)
            $(this).focus()

            return false
        }

    })

    // add to cart functionality

    $(".add-to-cart-btn").on("click", function(){
        let this_val = $(this)
        let index_value = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index_value).val()
        let product_title = $(".product-title-" + index_value).val()
        let product_id = $(".product-id-" + index_value).val()
        let product_price = $(".current-product-price-" + index_value).text()
        let product_pid = $(".product-pid-" + index_value).val()
        let product_image = $(".product-image-" + index_value).val()

        console.log("Quantity: ", quantity);
        console.log("Product title: ", product_title);
        console.log("Product ID: ", product_id);
        console.log("Price: ", product_price);
        console.log("Image: ", product_image);
        console.log("PID: ", product_pid)
        console.log("Current Element: ", this_val);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'quantity': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding products to Cart...")
            },
            success: function(response){
                this_val.html("<i class='fas fa-check-circle'></i>")
                console.log("Added Product to Cart!");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })

    // delete cart item

    $(document).on('click', '.delete-product', function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        console.log("Product ID:", product_id)

        $.ajax({
            url: '/delete-from-cart',
            data:{
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.prop('disabled', true)
            },
            success: function(response){
                this_val.prop('disabled', false)
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })



    $(document).on('click', '.update-product', function(){
        let product_id = $(this).attr("data-product");
        let product_quantity = $(".product-quantity-" + product_id).val();
        let this_val = $(this);
        console.log("Product ID:", product_id);
        console.log("Quantity: ", product_quantity);

        $.ajax({
            url: '/update-cart/',
            data: {
                'id': product_id,
                'quantity': product_quantity,
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.prop('disabled', true);
            },
            success: function(response){
                this_val.prop('disabled', false);
                console.log(response);
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
        });
    });


    // make addresses default
    $(document).on("click", ".make-address-default", function(){
        let address_id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("Address ID: ", address_id);
        console.log("Element is:", this_val)

        $.ajax({
            url: "/make-address-default",
            data: {
                "id": address_id,
            },
            dataType: "json",
            success: function(response){
                console.log("Address made Default");
                if (response.boolean == true){
                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+address_id).show()
                    $(".button"+address_id).hide()
                }
            }
        })
    })
})
