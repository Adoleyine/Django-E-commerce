from django.db import models
from django.db.models import Sum, F
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userAuths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATINGS = (
    ( 1, "★☆☆☆☆"),
    ( 2, "★★☆☆☆"),
    ( 3, "★★★☆☆"),
    ( 4, "★★★★☆"),
    ( 5, "★★★★★")
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)



class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="cateorgy.jpg")
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe(f'<img src = "{self.image.url}" width="50px" height="50" />')

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Charmy")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is a vendor")
    address = models.CharField(max_length=100, default="knust newsite, KNUST-Kumasi")
    contact = models.CharField(max_length=100, default=("+233 5457-63536"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paystack_payment_intent = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def calculate_revenue(self):
        # Calculate the revenue from all products sold by this vendor
        revenue = CartOrderItems.objects.filter(
            product__vendor=self,
            order__paid_status=True  # assuming 'paid_status' indicates a completed order
        ).aggregate(total_revenue=Sum(F('price') * F('quantity')))['total_revenue']

        return revenue or 0

    def calculate_number_of_orders(self):
        # Count the number of orders from all products sold by this vendor
        number_of_orders = CartOrderItems.objects.filter(
            product__vendor=self,
            order__paid_status=True  # assuming 'paid_status' indicates a completed order
        ).count()

        return number_of_orders


    def vendor_image(self):
        return mark_safe(f'<img src = "{self.image.url}" width="50px" height="50" />')
    
    def __str__(self):
        return self.title
    


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    price = models.DecimalField(decimal_places=2, max_digits=12, default=1.99)
    old_price = models.DecimalField(decimal_places=2, max_digits=12, default=1.99)
    specifications = RichTextUploadingField(null=True, blank=True)
    # extra
    stock_count = models.CharField(max_length=100, default="10",  null=True, blank=True)
    tags = TaggableManager(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor")
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review", null=True, blank=True)
    status = models.BooleanField(default=True)
    in_sock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    
    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe(f'<img src = "{self.image.url}" width="50px" height="50" />')
    
    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"






############################ Cart, Order, OrderItems

class  CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True, blank=True)
    
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    

    tracking_id = models.CharField(max_length=200, null=True, blank=True)
    
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    sku = ShortUUIDField(blank=True, null=True, length=5, max_length=20, prefix="sku", alphabet="abcdefgh1234")
    oid = ShortUUIDField(blank=True, null=True, length=5, max_length=20, alphabet="1234567890")

    class Meta:
        verbose_name_plural = "Cart Order"


class  CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=1.99)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=1.99)
    invoice_number = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Cart Order Items"

    def category_image(self):
        return mark_safe('<img src = "%s" width="50px" height="50" />' %(self.image.url))
    def order_image(self):
        return mark_safe('<img src = "/media/%s" width="50px" height="50" />' %(self.image))


#############################Product review, wishlists, Address

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATINGS, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    mobile = models.CharField(max_length=130, null=True)
    def __str__(self):
        return self.address
    class Meta:
        verbose_name_plural = "Address"



