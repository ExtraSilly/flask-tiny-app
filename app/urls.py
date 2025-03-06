from django.contrib import admin
from django.urls import path
from . import views
from .views import post_list, reset_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Trang chủ & xác thực người dùng
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),

    # Các trang quản lý giỏ hàng & danh sách lưu
    path('cart/', views.cart, name="cart"),
    path('saved/', views.saved, name="saved"),

    # CRUD Thành viên
    path('members/', views.members_list, name="member_list"),  # Đảm bảo tên URL chính xác
    
    path('add/', views.add, name="add"),
    path('addrec/', views.addrec, name="addrec"),
    path('index/', views.index, name="index"),
    path('index/delete/<int:id>/', views.delete, name='delete'),
    path('index/update/<int:id>/', views.update, name='update'),
    path('update/uprec/<int:id>/', views.uprec, name="uprec"),

    # Hành động chặn / bỏ chặn user
    path('block_user/<int:id>/', views.block_user, name="block_user"),
    path('unblock_user/<int:id>/', views.unblock_user, name="unblock_user"),

    # Reset mật khẩu cho user từ admin
    path('reset_password/<int:user_id>/', views.reset_password, name="reset_password"),

    # Chức năng reset password chung cho tất cả người dùng
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name="password_reset_complete"),

    # CRUD Bài viết
    path('posts/', views.post_list, name="post_list"),  # Trang danh sách bài viết
    path('posts/create/', views.create_post, name="create_post"),
    path('posts/update/<int:id>/', views.update_post, name="update_post"),  # Trang chỉnh sửa bài viết
    path('posts/delete/<int:id>/', views.delete_post, name="delete_post"),  # Trang xóa bài viết
]
