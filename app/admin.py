from django.contrib import admin

# Register your models here.
# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import Customer

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name', 'email', 'is_blocked')
#     actions = ['block_users', 'unblock_users', 'reset_passwords']

#     def block_users(self, request, queryset):
#         queryset.update(is_blocked=True)
#         self.message_user(request, "Người dùng đã bị khóa.")

#     def unblock_users(self, request, queryset):
#         queryset.update(is_blocked=False)
#         self.message_user(request, "Người dùng đã được mở khóa.")

#     def reset_passwords(self, request, queryset):
#         for customer in queryset:
#             customer.user.set_password("defaultpassword123")
#             customer.user.save()
#         self.message_user(request, "Mật khẩu của người dùng đã được đặt lại.")

#     block_users.short_description = "Khóa tài khoản người dùng"
#     unblock_users.short_description = "Mở khóa tài khoản người dùng"
#     reset_passwords.short_description = "Reset mật khẩu về mặc định"

# admin.site.register(Customer, CustomerAdmin)

