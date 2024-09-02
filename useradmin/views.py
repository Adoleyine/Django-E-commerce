from django.contrib.auth.decorators import login_required
from core.models import CartOrder, Product, Category, CartOrderItems, ProductReview, Vendor
from userAuths.models import User, Profile
import datetime
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from useradmin.forms import AddProductForm, VendorForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.db.models import Sum
@login_required
def dashboard(request):
    user = request.user
    is_admin = user.is_superuser

    if is_admin:
        # Admin dashboard
        revenue = CartOrder.objects.aggregate(price=Sum("price"))
        total_orders_count = CartOrder.objects.all()
        all_products = Product.objects.all()
        all_category = Category.objects.all()
        new_customers = User.objects.all().order_by("-id")
        latest_orders = CartOrder.objects.all().order_by("-id")
        this_month = datetime.datetime.now().month
        monthly_revenue = CartOrder.objects.filter(order_date__month=this_month, paid_status=True).aggregate(price=Sum("price"))

        # Revenue by vendor
        vendors = Vendor.objects.all()
        vendor_revenue = {}
        for vendor in vendors:
            vendor_products = Product.objects.filter(vendor=vendor)
            revenue_for_vendor = CartOrderItems.objects.filter(
                item__in=vendor_products
            ).aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
            vendor_revenue[vendor] = revenue_for_vendor

        context = {
            'revenue': revenue,
            'total_orders_count': total_orders_count,
            'all_products': all_products,
            'all_category': all_category,
            'new_customers': new_customers,
            'latest_orders': latest_orders,
            'monthly_revenue': monthly_revenue,
            'vendor_revenue': vendor_revenue,
        }
    else:
        # Normal user dashboard
        try:
            vendor = Vendor.objects.get(user=user)
        except Vendor.DoesNotExist:
            vendor = None

        if vendor:
            user_orders = CartOrder.objects.filter(user=user).order_by('-id')
            user_products = Product.objects.filter(vendor=vendor)
            user_revenue = CartOrderItems.objects.filter(
                order__in=user_orders,
                item__in=user_products, paid_status=True
            ).aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
        else:
            user_orders = []
            user_products = []
            user_revenue = 0

        context = {
            'user_orders': user_orders,
            'user_products': user_products,
            'user_revenue': user_revenue,
        }

    return render(request, 'useradmin/dashboard.html', context)


@login_required
def products(request):
    user = request.user
    if user.is_superuser:
        all_products = Product.objects.all().order_by('-id')
    else:
        all_products = Product.objects.filter(user=user).order_by('-id')
        
    all_category = Category.objects.all()

    context = {
        'all_products': all_products,
        'all_category': all_category,
    }
    return render(request, 'useradmin/products.html', context)


@login_required
def add_product(request):
    user = request.user
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user  # Set the user
            new_form.vendor = Vendor.objects.get(user=user)  #
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:dashboard')
    else:
        form = AddProductForm()

    context = {
        'form': form,
    }
    return render(request, 'useradmin/add_product.html', context)



@login_required
def edit_product(request, pid):
    user = request.user
    product = Product.objects.get(pid=pid)

    # Check if the user has permission to edit this product
    if product.user != user and not user.is_superuser:
        return redirect('useradmin:dashboard')

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user  # Set the user
            new_form.vendor = Vendor.objects.get(user=user)  #
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:edit-product', product.pid)
    else:
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'useradmin/edit_product.html', context)



@login_required
def delete_product(request, pid):
    user = request.user
    product = Product.objects.get(pid=pid)

    # Check if the user has permission to delete this product
    if product.user != user and not user.is_superuser:
        return redirect('useradmin:dashboard')

    product.delete()
    return redirect('useradmin:products')


@login_required
def orders(request):
    user = request.user
    if user.is_superuser:
        orders = CartOrder.objects.all().order_by('-id')
    else:
        orders = CartOrder.objects.filter(user=user)

    context = {
        'orders': orders,
    }
    return render(request, 'useradmin/orders.html', context)


@login_required
def order_detail(request, id):
    user = request.user
    order = CartOrder.objects.get(id=id)

    # Check if the user has permission to view this order
    if order.user != user and not user.is_superuser:
        return redirect('useradmin:dashboard')

    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'useradmin/order_detail.html', context)



@csrf_exempt
@login_required
def change_order_status(request, id):
    user = request.user
    order = CartOrder.objects.get(id=id)

    # Check if the user has permission to change the status
    if not user.is_superuser:
        return redirect('useradmin:dashboard')

    if request.method == 'POST':
        status = request.POST.get('status')
        order.product_status = status
        order.save()
        messages.success(request, f'Order status changed to {status}')
    
    return redirect('useradmin:order-detail', order.id)

def shop_page(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_sales = CartOrderItems.objects.filter(order__paid_status=True).aggregate(quantity=Sum("quantity"))
    context = {
        'products': products,
        'revenue': revenue,
        'total_sales': total_sales,
    }
    return render(request, 'useradmin/shop_page.html', context)


def reviews(request):
    reviews = ProductReview.objects.all()
    
    context = {
        "reviews": reviews
    }
    return render(request, 'useradmin/reviews.html', context)


def settings(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        
        if image != None:
            profile.image = image
        
        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        
        profile.save()
        messages.success(request, "Profile Updated")
        return redirect('useradmin:settings')
    
    context ={
        'profile': profile
    }
    
    return render(request, 'useradmin/settings.html', context)


def change_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        if confirm_new_password != new_password:
            messages.error(request, "Password does not match")
            return redirect('useradmin:settings')
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed")
            return redirect('useradmin:change-password')
        else:
            messages.error(request, "Old Password is incorrect")
            return redirect('useradmin:change-password')
    
    return render(request, 'useradmin/change_password.html')

def vendor_profile(request):
    # Try to get the vendor profile for the current user
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None

    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('useradmin:dashboard')
    else:
        form = VendorForm(instance=vendor)

    return render(request, 'useradmin/create_vendor.html', {'form': form})
def create_vendor_profile(request):
   pass