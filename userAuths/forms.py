from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.context_processor import default
from userAuths.models import User, Profile

# This form helps in the creation of users using django default form module
USER_ROLE = [
    ('', 'Select User'),
    ('vendor', 'Vendor'),
    ('customer', 'Customer'),
]
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    role = forms.ChoiceField(choices=USER_ROLE,widget=forms.Select(attrs={"class":"select-active"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

# This form is used in the creation of a user profile
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']