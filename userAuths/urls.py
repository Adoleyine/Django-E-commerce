from tkinter.font import names

from django.urls import path
from . import views


app_name = 'userAuths'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('sign-out/', views.logout_view, name='sign-out'),
    path('logout-sign-up', views.custom_logout_signup, name='logout-sign-up'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),

]
