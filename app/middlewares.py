# from django.shortcuts import redirect
# from django.contrib import messages
# from .models import Customer

# class BlockUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             try:
#                 customer = Customer.objects.get(user=request.user)
#                 if customer.is_blocked:
#                     messages.error(request, "Tài khoản của bạn đã bị khóa.")
#                     logout(request)
#                     return redirect('login')
#             except Customer.DoesNotExist:
#                 pass  # Nếu user không có Customer profile, không làm gì cả
        
#         return self.get_response(request)
