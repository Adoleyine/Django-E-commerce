from django.urls import path, include
from . import views


# app name
app_name = 'core'

urlpatterns = [
    # HomePage
    path('',views.index, name='index'),
    path('products/', views.product_list, name='product-list'),
    path('product/<pid>/', views.product_detail, name='product-detail'),
    
    # Category
    path('category/', views.category_list, name='category-list'),
    path('category/<cid>/', views.category_product_list, name='category-product-list'),
    
    # Vendor
    path('vendor/', views.vendor_list, name='vendor-list'),
    path('vendor/<vid>/', views.vendor_detail, name='vendor-detail'),
    
    # Tags
    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),
    
    # Reviews
    path('review_form/<str:pid>/', views.review_form, name='add-review-form'),
    
    # Search
    path('search/', views.search_view, name='search'),
    
    # Filter
    path('filter-product/', views.filter_product, name="filter-product"),
    
    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    # list cart
    path('cart/', views.cart, name='cart'), 
    
    # delete cart item
    path('delete-from-cart/', views.delete_item_from_cart, name="delete-from-cart"),
    
    # update cart items
    path('update-cart/', views.update_cart, name='update-cart'),
    
    # checkout
    path('checkout/<oid>/', views.checkout, name='checkout'),
    
    # payment successful
    path('payment-successful/<oid>/', views.payment_successful, name='payment-successful'),
    
    # payment failed
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    
    # payment completed
    path('payment-completed/', views.payment_completed, name='payment-completed'),
    
    # dashboard
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    
    # order details
    path('dashboard/order/<int:id>', views.order_detail, name='order-detail'),
    
    # default address
    path('make-address-default', views.make_address_default, name='make-address-default'),
    
    
    path("save-checkout-info/", views.save_checkoutInfo, name="save-checkout-info")
]
