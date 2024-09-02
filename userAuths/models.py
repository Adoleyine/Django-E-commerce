from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.
USER_ROLE = [
    ('', 'Select User'),
    ('vendor', 'Vendor'),
    ('customer', 'Customer'),
]
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=USER_ROLE, default=None)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    phone = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.full_name
        except:
            return self.user
    @property
    def email(self):
        return self.user.email


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)