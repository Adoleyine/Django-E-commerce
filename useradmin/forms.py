from core.models import Product, Vendor, ProductImages
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from taggit.forms import TagField

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter product Title", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Product description ...", "class": "form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Sale Price", "class": "form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Old Price", "class": "form-control"}))
    stock_count = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "How many products are in stock?", "class": "form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))
    product_status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={"class": "form-control select-active"}))
    specifications = forms.CharField(widget=CKEditorUploadingWidget(attrs={"placeholder": "Product specification ...", "class": "form-control"}))
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'category',
            'specifications',
            'tags',
            'in_sock',
            'stock_count',
            'product_status',
        ]
class VendorForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter vendor name", "class": "form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))
    cover_image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Vendor description ...", "class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Vendor address", "class": "form-control"}))
    contact = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Contact number", "class": "form-control"}))

    class Meta:
        model = Vendor
        fields = [
            'title',
            'image',
            'cover_image',
            'description',
            'address',
            'contact',
        ]