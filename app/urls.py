from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name ="register"),
    path('login/', views.loginPage, name ="login"),
    path('logout/', views.logoutPage, name ="logout"),
    path('cart/', views.cart, name ="cart"),
    path('saved/', views.saved, name ="saved"),
    
]