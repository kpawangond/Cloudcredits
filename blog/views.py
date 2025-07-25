
from blogApp.models import Category,Blog
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import RegisterForm,LoginForm
from django.contrib import messages


def home(request):
    category = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True ,status='published')
    latest_posts=Blog.objects.filter(is_featured=False,status='published').order_by('-created_at')[:5]
    context = {
        'category': category,
        'featured_posts': featured_posts,
        'latest_posts':latest_posts
    }
    return render(request, 'home.html', context)

# Registration method
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# login method
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user) 
                return redirect('home')  
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#logout_view 
def logout_view(request):
    logout(request) 
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

