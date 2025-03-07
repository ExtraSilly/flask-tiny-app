from django.contrib import admin
from .models import Member
from .models import *
from django.contrib import admin
from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "firstname", "lastname", "country")  # Thêm user vào list_display
    search_fields = ("user__username", "firstname", "lastname")  # Thêm tìm kiếm theo user
    list_filter = ("country",)  # Lọc theo quốc gia nếu cần




admin.site.register(Member,MemberAdmin)

admin.site.register(Customer)
admin.site.register(Product)

