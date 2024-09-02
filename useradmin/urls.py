from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('vendor-profile', views.vendor_profile, name='vendor-profile'),
    path('vendor/', views.create_vendor_profile, name='create_vendor_profile'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit-product/<pid>/', views.edit_product, name='edit-product'),
    path('delete-product/<pid>', views.delete_product, name='delete-product'),
    path('orders', views.orders, name='orders'),
    path('order-detail/<id>/', views.order_detail, name='order-detail'),
    path('change-order-status/<id>/', views.change_order_status, name='change-order-status'),
    path('shop-page/', views.shop_page, name='shop-page'),
    path('reviews/', views.reviews, name='reviews'),
    path('settings/', views.settings, name='settings'),
    path('change-password/', views.change_password, name='change-password'),

    


]
