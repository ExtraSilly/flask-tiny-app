from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from app.models import Post
from django.db.models import Count


def index(request):
    mem=Member.objects.all()
    return render(request,'app/index.html',{'mem':mem})

def add(request):
    return render(request,'app/add.html')

def addrec(request):
    x=request.POST['first']
    y=request.POST['last']
    z=request.POST['country']
    mem=Member(firstname=x,lastname=y,country=z)
    mem.save()
    return redirect("index")

def delete(request,id):
    mem=Member.objects.get(id=id)
    mem.delete()
    return redirect("index")

def update(request,id):
    mem=Member.objects.get(id=id)
    return render(request,'app/update.html',{'mem':mem})

def uprec(request,id):
    x=request.POST['first']
    y=request.POST['last']
    z=request.POST['country']
    mem=Member.objects.get(id=id)
    mem.firstname=x
    mem.lastname=y
    mem.country=z
    mem.save()
    return redirect("index")



def register(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo Customer tự động khi đăng ký thành công
            Customer.objects.create(user=user, name=user.first_name, email=user.email)

            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect("login")
        else:
            messages.error(request, "Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")

    context = {'form': form, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/register.html', context)




def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")  # Nếu user đã đăng nhập, chuyển về trang chủ

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:  # Kiểm tra trạng thái tài khoản
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.")
                return render(request, "app/login.html")  # QUAN TRỌNG: Render lại trang login để giữ thông báo
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")

    return render(request, "app/login.html")  # Render trang login


def logoutPage(request):
    logout(request)
    return redirect("login")
def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'products': products,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/home.html',context)

def cart(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'app/cart.html', context)
def saved(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.filter(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
    context = {'items':items,'order':order}
    
    return render(request, 'app/saved.html', context)


@login_required
def create_post(request):
    print("Debug: Đã vào view create_post")  # Kiểm tra xem function này có chạy không
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Gán user hiện tại làm tác giả
            post.save()
            messages.success(request, "Bài viết đã được đăng thành công!")
            return redirect("post_list")
    else:
        form = PostForm()
    
    return render(request, 'app/create_post.html', {'form': form})



def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Lấy tất cả bài viết, sắp xếp mới nhất trước
    total_posts = posts.count()  # Đếm tổng số bài viết

    paginator = Paginator(posts, 10)  # Mỗi trang hiển thị 10 bài viết
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    posts_page = paginator.get_page(page_number)  # Lấy dữ liệu của trang hiện tại

    return render(request, 'app/post_list.html', {
        'posts': posts_page,  # Chỉ gửi dữ liệu của trang hiện tại
        'total_posts': total_posts,
    })



@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Bài viết đã được cập nhật!")
            return redirect("post_list")
    else:
        form = PostForm(instance=post)
    
    return render(request, 'app/update_post.html', {'form': form})


@login_required
def delete_post(request, id):
    # Lấy bài viết
    post = get_object_or_404(Post, id=id)

    # Kiểm tra quyền: Admin có thể xóa tất cả, user chỉ xóa bài của họ
    if request.user == post.author or request.user.is_superuser:
        if request.method == "POST":
            post.delete()
            messages.success(request, "Bài viết đã bị xóa!")
            return redirect("post_list")
    else:
        messages.error(request, "Bạn không có quyền xóa bài viết này!")
        return redirect("post_list")

    return render(request, 'app/delete_post.html', {'post': post})

@login_required
def members_list(request):
    # Lấy danh sách thành viên và đảm bảo user không bị mất liên kết
    members = Member.objects.select_related('user').all()

    for member in members:
        if member.user:  # Kiểm tra nếu user tồn tại
            member.post_count = Post.objects.filter(author=member.user).count()
        else:
            member.post_count = 0  # Nếu không có user, gán 0 bài viết

    return render(request, 'app/members.html', {'mem': members})

@login_required
def block_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.is_superuser:
        user.is_active = False
        user.save()
        messages.success(request, f"Đã khóa tài khoản {user.username}.")
    else:
        messages.error(request, "Bạn không có quyền thực hiện thao tác này.")

    return redirect(reverse('index'))  # Chuyển hướng về trang index

@login_required
def unblock_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.is_superuser:
        user.is_active = True
        user.save()
        messages.success(request, f"Đã mở khóa tài khoản {user.username}.")
    else:
        messages.error(request, "Bạn không có quyền thực hiện thao tác này.")

    return redirect(reverse('index'))  # Chuyển hướng về trang index

@staff_member_required
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mật khẩu của {user.username} đã được cập nhật.")
            return redirect(reverse("member_list"))  # Điều hướng về danh sách thành viên
    else:
        form = AdminPasswordChangeForm(user)

    return render(request, "app/reset_password.html", {"form": form, "user": user})
