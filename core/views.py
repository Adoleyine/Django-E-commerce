from decimal import Decimal
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Address
from userAuths.models import  Profile
from taggit.models import Tag
from django.db.models import Avg, Q
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    # products  = Product.objects.all().order_by("-id") 

    products = Product.objects.filter(product_status="published") # only display products that are featured and their status is published
    context = {
        'products': products,
        }
    return render(request, 'core/index.html', context)


def product_list(request):
    products = Product.objects.filter(product_status="published")
    
    context = {'products': products}
    
    return render(request, 'core/product-list.html', context)


def category_list(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }

    return render(request, 'core/category_list.html', context)


def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category=category, product_status="published")
    context = {
        'category':category,
        'products': products
    }
    
    return render(request, 'core/category-product-list.html', context)


def vendor_list(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor_list.html', context)


def vendor_detail(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    
    context = {
        'vendor':vendor,
        'products': products
    }
    
    return render(request, 'core/vendor_detail.html', context)


def product_detail(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    review_form = ProductReviewForm()
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    product_image = product.product_images.all()
    address = Address.objects.get(status=True)
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False
    context = {
        'review_form':review_form,
        'make_review': make_review,
        'product': product,
        'product_image': product_image,
        'products': products,
        'reviews': reviews,
        'avg': average_rating,
        'address': address,
    }
    
    return render(request, 'core/product_detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by('-date')
    
    tag = None
    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    context = {
        'products': products,
        'tag': tag,
    }
    
    return render(request, 'core/tag.html', context)


def review_form(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['review'],
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('-date')
    vendors = Vendor.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
    context = {
        'products': products,
        'query': query,
        'vendors': vendors,
    }
    return render(request, 'core/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    
    context =  {
        'products': products,
    }
    data = render_to_string("core/async/product_list.html", context)
    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'quantity': request.GET['quantity'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid']
    }
    print( request.GET['price'])
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = int(cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            print(item['price'])
            cart_total_amount += int(item['quantity']) * float(item['price'])
            print(cart_total_amount)

        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your Cart is Empty")
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
             cart_total_amount += int(item['quantity']) * float(item['price'])
        
    context = render_to_string("core/async/cart_list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})    
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    quantity = request.GET['quantity']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = quantity
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
             cart_total_amount += int(item['quantity']) * float(item['price'])
        
    context = render_to_string("core/async/cart_list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})    
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})

def save_checkoutInfo(request):
    cart_total_amount = 0
    total_amount = 0

    # getting values from forms
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        # saving values from form to the current session
        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['address'] = address
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country

    # checks if session exist
        if 'cart_data_obj' in request.session:

            for product_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['quantity']) * float(item['price'])

            # save data to the CartOrder model
            order = CartOrder.objects.create(
                user = request.user,
                price = total_amount,
                full_name = full_name,
                email = email,
                phone = phone,
                address = address,
                city = city,
                state = state,
                country = country,
            )
            # after saving the data to the model delete data from session
            del request.session['full_name']
            del request.session['email']
            del request.session['phone']
            del request.session['address']
            del request.session['city']
            del request.session['state']
            del request.session['country']

            # total amount for cart
            for product_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['quantity']) * float(item['price'])

                cart_order_items = CartOrderItems.objects.create(
                    order = order,
                    invoice_number = 'INVOICE_NO-' + str(order.id),
                    item = item['title'],
                    price = item['price'],
                    quantity = item['quantity'],
                    image = item['image'],
                    total = float(item['price']) * float(item['quantity'])
                )

        return redirect("core:checkout", order.oid)


def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)
    order_total = order.price * 100
    context = {
        "order": order,
        "order_items": order_items,
        'order_total': order_total,
    }
    return render(request, 'core/checkout.html', context)

@login_required
def payment_successful(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
    context = {
        'order': order
    }
    return render(request, 'core/payment_successful.html', context)



@login_required
def payment_failed(request):
    return render(request, 'core/payment_failed.html')


def payment_completed(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
             cart_total_amount += int(item['quantity']) * float(item['price'])
    return render(request, "core/payment_completed.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    email =  profile.email
    if request.method == "POST":
        address = request.POST.get('address')
        mobile = request.POST.get('phone')
        new_address = Address.objects.create(
            user = request.user,
            address = address,
            mobile = mobile
        )
        messages.success(request, "Address Added Successfully")
        return redirect("core:dashboard")

    context = {
        "email": email,
        "profile": profile,
        "orders": orders,
        "address": address,
    }
    return render(request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    context = {
        "products": products
    }
    return render(request, 'core/order_detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})
